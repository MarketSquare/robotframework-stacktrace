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
from robot.libraries.BuiltIn import BuiltIn

__version__ = '0.0.2'

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
        self.resolved_args = res_args or []
        self.kind = kind


class RobotStackTracer:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.StackTrace = []
        self.new_error = True
        self.suite_source = None
        self.errormessage = ""

    def start_suite(self, name, attrs):
        self.StackTrace = [StackTrace(attrs["source"], None, name, kind=Kind.Suite)]
        self.suite_source = attrs["source"]

    def start_test(self, name, attrs):
        self.StackTrace.append(
            StackTrace(self.suite_source, attrs["lineno"], name, kind=Kind.Test)
        )

    def start_keyword(self, name, attrs):
        self.StackTrace.append(
            StackTrace(attrs["source"], attrs["lineno"], attrs["kwname"], attrs["args"], [bi.replace_variables(arg) for arg in attrs["args"]])
        )
        self.new_error = True

    def end_keyword(self, name, attrs):
        if attrs["status"] == "FAIL" and self.new_error:
            print(f"\nTraceback (most recent call last):")
            call: StackTrace
            for index, call in enumerate(self.StackTrace):
                if call.kind >= Kind.Test:
                    path = (
                        f"{call.source}:{call.lineno}"
                        if call.lineno and call.lineno > 0
                        else f"{call.source}:0"
                    )
                    print(f'  File  "{path}"')
                    print(f'  >  {call.name}    {"    ".join(call.args)}')
                    if call.args != call.resolved_args:
                        print(f'  E  {call.name}    {"    ".join(call.resolved_args)}')
        self.StackTrace.pop()
        self.new_error = False

    def end_test(self, name, attrs):
        if attrs["status"] == "FAIL":
            self.lineno = attrs["lineno"]
        self.StackTrace.pop()

    def end_suite(self, name, attrs):
        self.StackTrace = []

    def log_message(self, message):
        if message["level"] == "FAIL":
            self.errormessage = message["message"]
