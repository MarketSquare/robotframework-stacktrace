*** Test Case ***
Side effect in variable resolving
    ${d}=   Create Dictionary  x=a  y=b
    ${res}=   Set Variable   ${d.pop('x')}

Side effect in variable resolving FAILING
    ${d}=   Create Dictionary  x=a  y=b
    Fail   ${d.pop('x')}
