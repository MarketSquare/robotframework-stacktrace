*** Settings ***
Suite Setup    Log    Logs some Start
Suite Teardown      Keyword That Calls a Failing one

*** Test Cases ***
first teardown fail
    [Setup]     Log    This is something
    Log     Hello
    [Teardown]    Fail    by purpose

Second setup fails
    [Setup]    Keyword That Calls a Failing one
    Log     I will Never Be called
    [Teardown]      Fail    this fails as well


*** Keywords ***
Keyword That Calls a Failing one
    Keyword that fails

Keyword that fails
    Should Be True    False
