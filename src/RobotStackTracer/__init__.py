# Copyright 2020-  René Rohner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import IntEnum

from robot.errors import VariableError
from robot.libraries.BuiltIn import BuiltIn

__version__ = '0.2.0'

bi = BuiltIn()


class Kind(IntEnum):
    Suite = 0
    Test = 1
    Keyword = 2


class StackTrace:
    def __init__(self, source, lineno, name, args=None, res_args=None, kind: Kind = Kind.Keyword):
        self.source = source
        self.lineno = lineno
        self.name = name
        self.args = args or []
        self.resolved_args = res_args or {}
        self.kind = kind


class RobotStackTracer:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.StackTrace = []
        self.last_error = None
        self.new_error = True
        self.suite_source = None
        self.errormessage = ""

    def start_suite(self, name, attrs):
        self.StackTrace = [StackTrace(attrs["source"], None, name, kind=Kind.Suite)]
        self.suite_source = attrs["source"]

    def start_test(self, name, attrs):
        self.StackTrace.append(StackTrace(self.suite_source, attrs["lineno"], name, kind=Kind.Test))

    def start_keyword(self, name, attrs):
        self.StackTrace.append(
            StackTrace(
                attrs["source"],
                attrs["lineno"],
                attrs["kwname"],
                attrs["args"],
                self.resolve_variables(attrs),
            )
        )
        self.new_error = True

    def resolve_variables(self, attrs):
        res_args = {}
        for arg in attrs["args"]:
            try:
                resolved = bi.replace_variables(arg)
                if resolved != arg:
                    res_args[str(arg)] = f'{resolved} ({type(resolved).__name__})'
            except VariableError:
                res_args[str(arg)] = '<VariableError>'
        return res_args

    def end_keyword(self, name, attrs):
        if attrs["status"] == "FAIL" and self.new_error:
            self.last_error = self._create_stacktrace_text()
        self.StackTrace.pop()
        self.new_error = False

    def _create_stacktrace_text(self) -> str:
        error_text = [f'  ']
        error_text += ["  Traceback (most recent call last):"]
        call: StackTrace
        for index, call in enumerate(self.StackTrace):
            if call.kind >= Kind.Test:
                path = (
                    f"{call.source}:{call.lineno}"
                    if call.lineno and call.lineno > 0
                    else f"{call.source}:0"
                )
                error_text += [f'    {"~" * 74}']
                error_text += [f'    File  "{path}"']
                error_text += [f'      {call.name}    {"    ".join(call.args)}']
                for var, value in call.resolved_args.items():
                    error_text += [f'      |  {var} = {value}']
        error_text += [f'{"_" * 78}']
        return error_text

    def end_test(self, name, attrs):
        if attrs["status"] == "FAIL":
            print("\n".join(self.last_error))
            self.lineno = attrs["lineno"]
        self.StackTrace.pop()
        self.last_error = None

    def end_suite(self, name, attrs):
        self.StackTrace = []

    def log_message(self, message):
        if message["level"] == "FAIL":
            self.errormessage = message["message"]
