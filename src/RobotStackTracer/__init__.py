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
from os import path

from robot.errors import VariableError
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import cut_long_message

__version__ = '0.4.0'

bi = BuiltIn()

muting_keywords = [
    "Run Keyword And Ignore Error",
    "Run Keyword And Expect Error",
    "Run Keyword And Return Status",
    "Run Keyword And Warn On Failure",
    "Wait Until Keyword Succeeds",
]


class Kind(IntEnum):
    Suite = 0
    Test = 1
    Keyword = 2


class StackElement:
    def __init__(
        self, file, source, lineno, name, args=None, res_args=None, kind: Kind = Kind.Keyword
    ):
        self.file = file
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
        self.SuiteTrace = []
        self.new_error = True
        self.errormessage = ""
        self.mutings = []
        self.lib_files = {}

    def start_suite(self, name, attrs):
        self.SuiteTrace.append(attrs["source"])

    def library_import(self, name, attrs):
        self.lib_files[name] = attrs.get('source')

    def resource_import(self, name, attrs):
        self.lib_files[name] = attrs.get('source')

    def start_test(self, name, attrs):
        self.StackTrace = [
            StackElement(
                self.SuiteTrace[-1], self.SuiteTrace[-1], attrs["lineno"], name, kind=Kind.Test
            )
        ]

    def start_keyword(self, name, attrs):
        source = attrs.get(
            'source', self.StackTrace[-1].file if self.StackTrace else self.SuiteTrace[-1]
        )
        file = self.lib_files.get(attrs.get('libname'), source)

        self.StackTrace.append(
            StackElement(
                file,
                self.fix_source(source),
                attrs.get('lineno', None),
                attrs['kwname'],
                attrs['args'],
                self.resolve_variables(attrs),
            )
        )
        if attrs['kwname'] in muting_keywords:
            self.mutings.append(attrs['kwname'])
        self.new_error = True

    def fix_source(self, source):
        if source and path.isdir(source) and path.isfile(path.join(source, '__init__.robot')):
            return path.join(source, '__init__.robot')
        else:
            return source

    def resolve_variables(self, attrs):
        res_args = {}
        for arg in attrs["args"]:
            try:
                resolved = bi.replace_variables(arg)
                if resolved != arg:
                    res_args[str(arg)] = f'{resolved} ({type(resolved).__name__})'
            except VariableError:
                res_args[str(arg)] = '<Variable does not yet exist.>'
        return res_args

    def end_keyword(self, name, attrs):
        if self.mutings and attrs['kwname'] == self.mutings[-1]:
            self.mutings.pop()
        if attrs["status"] == "FAIL" and self.new_error and not self.mutings:
            print("\n".join(self._create_stacktrace_text()))
        self.StackTrace.pop()
        self.new_error = False

    def _create_stacktrace_text(self) -> str:
        error_text = [f'  ']
        error_text += ["  Traceback (most recent call last):"]
        call: StackElement
        for index, call in enumerate(self.StackTrace):
            if call.kind >= Kind.Test:
                kind = "T:" if call.kind == Kind.Test else ""
                path = (
                    f"{call.source}:{call.lineno}"
                    if call.lineno and call.lineno > 0
                    else f"{call.source}:0"
                )
                error_text += [f'    {"~" * 74}']
                error_text += [f'    File  {path}']
                error_text += [f'    {kind}  {call.name}    {"    ".join(call.args or [])}']
                for var, value in call.resolved_args.items():
                    error_text += [f'      |  {var} = {cut_long_message(value)}']
        error_text += [f'{"_" * 78}']
        return error_text

    def end_test(self, name, attrs):
        self.StackTrace = []

    def end_suite(self, name, attrs):
        self.SuiteTrace.pop()

    def log_message(self, message):
        if message["level"] == "FAIL":
            self.errormessage = message["message"]  # may be relevant / Not used
