*** Settings ***



*** Test Cases ***
Run Keyword
    Run Keyword    Log    Hello
    Run Keyword    Top Level One

Run Keyword And Ignore Error
    Run Keyword And Ignore Error    Should not print Stack Trace

Run Keyword And Continue On Failure
    Run Keyword And Continue On Failure    Top Level One     1st Error
    Run Keyword And Continue On Failure    Top Level One     2nd Error
    Run Keyword And Continue On Failure    Top Level One     3rd Error
    Run Keyword And Continue On Failure    Top Level One     4th Error
    Run Keyword And Continue On Failure    Top Level One     5th Error

Run Keyword And Expect Error
    Run Keyword and expect error    *    Top Level One    This is fine!

Run Keyword And Return
    This runs and returns error

Run Keyword And Return If
    This runs if and returns error

Run Keyword And Return Status
    ${status}    Run Keyword And Return Status    Should not print Stack Trace
    Should Be True    ${status}

Run Keyword And Warn On Failure
    Run Keyword And Warn On Failure    Top Level One     This should basically be a warning

Run Keywords
    Run Keywords    Log    Test
    ...   AND       Log Many    one    two    three
    ...   AND       Fail    with a message
    ...   AND       Log to console    Nothing

Pass WUKS
    Set Global Variable    ${counter}    ${0}
    Wait Until Keyword Succeeds    15 times    10 ms    Fails some times    ${10}

Fail in WUKS
    Set Global Variable    ${counter}    ${0}
    Wait Until Keyword Succeeds    9 times    10 ms    Fails some times    ${10}


*** Keywords ***
This runs and returns error
    Run Keyword And Return    Evaluate    " ".join(None)

This runs if and returns error
    Run Keyword And Return If    1 + 1 == 2    Evaluate    " ".join(None)

Should not print Stack Trace
    Fail    NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

Top Level One
    [Arguments]     ${message}=This one fails
    Low Level One    ${message}

Low Level One
    [Arguments]    ${message}
    Fail    ${message}

Fails some times
    [Arguments]    ${times}
    ${value}    Set Variable    ${counter}
    Set Global Variable    ${counter}    ${value+1}
    Should Be Equal    ${times}    ${counter}
