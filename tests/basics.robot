*** Settings ***
Library    Collections
Library    OperatingSystem
Resource    keywords.resource

*** Variables ***
${variable}     scalar content
&{dict}     key1=value1  key2=value2
@{list}    one    two    three

*** Test Cases ***
PASS Testing 1
   Log  passes

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

Fail with number
    ${var}    Set variable   ${1775675}
    Should be equal   ${var}  23



Fails with Unknown Variable
    Log    ${unknown_var}

Fail a compount
    Fail     this is a ${variable} text with a ${list}

Wrong If
    Log    Test
    IF   time.seven
        log    test
    END

*** Keywords ***
Keyword
   Keyword2

Check a List
    [Arguments]     ${list}
    Lists Should Be Equal    ${list}     ${{["one","two",3]}}

Check Dict
    [Arguments]     ${dict}
    Dictionary Should Contain Key    ${dict}    key
    
Fail Expanded
    [Arguments]     @{vargs}
    Fail    ${vargs}
