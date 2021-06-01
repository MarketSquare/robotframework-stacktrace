# robotframework-stacktrace
A listener for RF >= 4.0 that prints a Stack Trace to console to faster find the code section where the failure appears.

## Installation

```shell
pip install robotframework-stacktrace
```

## Usage

```shell
robot --listener RobotStackTracer <your file.robot>
```

### Example

Old Console Output:

```
robot -d logs TestCases/14_Browser/01_CarConfig.robot
==============================================================================
01 CarConfig                                                                  
==============================================================================
Configure Car with Pass                                               | FAIL |
TimeoutError: page.selectOption: Timeout 3000ms exceeded.
=========================== logs ===========================
waiting for selector ""Basismodell" >> ../.. >> select"
  selector resolved to visible <select _ngcontent-c7="" class="maxWidth ng-untouched ng…>…</select>
  selecting specified option(s)
    did not find some options - waiting... 
============================================================
Note: use DEBUG=pw:api environment variable to capture Playwright logs.
------------------------------------------------------------------------------
Configure Car with wrong Acc                                          | FAIL |
TimeoutError: page.check: Timeout 3000ms exceeded.
=========================== logs ===========================
waiting for selector "//span[contains(text(),'aABS')]/../input"
============================================================
Note: use DEBUG=pw:api environment variable to capture Playwright logs.
------------------------------------------------------------------------------
Configure Car with car Acc                                            | FAIL |
TimeoutError: page.click: Timeout 3000ms exceeded.
=========================== logs ===========================
waiting for selector "[href="/config/summary/wrong"]"
============================================================
Note: use DEBUG=pw:api environment variable to capture Playwright logs.
------------------------------------------------------------------------------
01 CarConfig                                                          | FAIL |
3 tests, 0 passed, 3 failed
==============================================================================
Output:  /Source/RF-Schulung/02_RobotFiles/logs/output.xml
Log:     /Source/RF-Schulung/02_RobotFiles/logs/log.html
Report:  /Source/RF-Schulung/02_RobotFiles/logs/report.html
```

New Stack Trace Output

```
 robot -d logs --listener RobotStackTracer TestCases/14_Browser/01_CarConfig.robot
==============================================================================
01 CarConfig                                                                  
==============================================================================
Configure Car with Pass                                               ..
Traceback (most recent call last):
  File  "/Source/RF-Schulung/02_RobotFiles/TestCases/14_Browser/01_CarConfig.robot:23", in "01 CarConfig"
    Configure Car with Pass    
  File  "/Source/RF-Schulung/02_RobotFiles/TestCases/14_Browser/01_CarConfig.robot:27", in "Configure Car with Pass"
    Select aMinigolf as model    
  File  "/Source/RF-Schulung/02_RobotFiles/TestCases/14_Browser/functional_keywords.resource:14", in "Select aMinigolf as model"
    Select Options By    ${select_CarBaseModel}    text    ${basemodel}
Configure Car with Pass                                               | FAIL |
TimeoutError: page.selectOption: Timeout 3000ms exceeded.
=========================== logs ===========================
waiting for selector ""Basismodell" >> ../.. >> select"
  selector resolved to visible <select _ngcontent-c7="" class="maxWidth ng-untouched ng…>…</select>
  selecting specified option(s)
    did not find some options - waiting... 
============================================================
Note: use DEBUG=pw:api environment variable to capture Playwright logs.
------------------------------------------------------------------------------
Configure Car with wrong Acc                                          ....
Traceback (most recent call last):
  File  "/Source/RF-Schulung/02_RobotFiles/TestCases/14_Browser/01_CarConfig.robot:37", in "01 CarConfig"
    Configure Car with wrong Acc    
  File  "/Source/RF-Schulung/02_RobotFiles/TestCases/14_Browser/01_CarConfig.robot:42", in "Configure Car with wrong Acc"
    Select Accessory    aABS
  File  "/Source/RF-Schulung/02_RobotFiles/TestCases/14_Browser/functional_keywords.resource:38", in "Select Accessory"
    Check Checkbox    //span[contains(text(),'${accessory}')]/../input
Configure Car with wrong Acc                                          | FAIL |
TimeoutError: page.check: Timeout 3000ms exceeded.
=========================== logs ===========================
waiting for selector "//span[contains(text(),'aABS')]/../input"
============================================================
Note: use DEBUG=pw:api environment variable to capture Playwright logs.
------------------------------------------------------------------------------
Configure Car with car Acc                                            ..      
Traceback (most recent call last):
  File  "/Source/RF-Schulung/02_RobotFiles/TestCases/14_Browser/01_CarConfig.robot:50", in "01 CarConfig"
    Configure Car with car Acc    
  File  "/Source/RF-Schulung/02_RobotFiles/TestCases/14_Browser/01_CarConfig.robot:61", in "Configure Car with car Acc"
    Set wrong Car Name    ${car}
  File  "/Source/RF-Schulung/02_RobotFiles/TestCases/14_Browser/functional_keywords.resource:53", in "Set wrong Car Name"
    Click    ${car_name}
Configure Car with car Acc                                            | FAIL |
TimeoutError: page.click: Timeout 3000ms exceeded.
=========================== logs ===========================
waiting for selector "[href="/config/summary/wrong"]"
============================================================
Note: use DEBUG=pw:api environment variable to capture Playwright logs.
------------------------------------------------------------------------------
01 CarConfig                                                          | FAIL |
3 tests, 0 passed, 3 failed
==============================================================================
Output:  /Source/RF-Schulung/02_RobotFiles/logs/output.xml
Log:     /Source/RF-Schulung/02_RobotFiles/logs/log.html
Report:  /Source/RF-Schulung/02_RobotFiles/logs/report.html
```