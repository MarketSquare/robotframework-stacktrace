*** Settings ***
Library    Collections
Library    OperatingSystem

*** Variables ***
${variable}     scalar content
&{dict}     key1=value1  key2=value2
@{list}    one    two    three

*** Test Cases ***
PASS Testing 1
   Log  passes

PASS Testing 2
   Run Keyword and expect error  *  Keyword2

PASS Testing 3
   Run Keyword And Ignore Error    Keyword2

Pass WUKS
    Set Global Variable    ${counter}    ${0}
    Wait Until Keyword Succeeds    15 times    10 ms    Fails some times    ${10}

Testing 1
   Should be equal    1    2

Testing 2
   Keyword

Resolve Variable
   Fail  ${variable}

Fail with a List
    Check a List    ${list}
    
Fail with dict
    Check Dict    ${dict}
    
Fail expanded keys
    Fail Expanded    &{dict}

Fail expanded items
    Fail Expanded    @{dict}

Fail expanded list
    Fail Expanded    @{list}

Fail with large file
    ${pure_vomit}=  Get File  ${CURDIR}/vomit.dat
    Should be equal   ${pure_vomit}  puke

Fail in WUKS
    Set Global Variable    ${counter}    ${0}
    Wait Until Keyword Succeeds    9 times    10 ms    Fails some times    ${10}

Fails with Unknown Variable
    Log    ${unknown_var}

Fail a compount
    Fail     this is a ${variable} text with a ${list}

*** Keywords ***
Keyword
   Keyword2

Keyword2
   Fail  for best reason

Check a List
    [Arguments]     ${list}
    Lists Should Be Equal    ${list}     ${{["one","two",3]}}

Check Dict
    [Arguments]     ${dict}
    Dictionary Should Contain Key    ${dict}    key
    
Fail Expanded
    [Arguments]     @{vargs}
    Fail    ${vargs}

Fails some times
    [Arguments]    ${times}
    ${value}    Set Variable    ${counter}
    Set Global Variable    ${counter}    ${value+1}
    Should Be Equal    ${times}    ${counter}