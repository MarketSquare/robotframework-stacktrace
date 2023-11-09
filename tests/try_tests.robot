*** Test Cases ***
TRY EXCEPT fail
    TRY
        Should be equal  1  2
    EXCEPT
        No Operation
    END

TRY EXCEPT pass
    TRY
        Should be equal  1  1
    EXCEPT
        No Operation
    END

TRY FINALLY fail
    TRY
        Should be equal  1  2
    FINALLY
        No Operation
    END

TRY FINALLY pass
    TRY
        Should be equal  1  1
    FINALLY
        No Operation
    END

TRY EXPECT FINALLY fail
    TRY
        Should be equal  1  2
    EXCEPT
        No Operation
    FINALLY
        No Operation
    END

TRY EXPECT FINALLY pass
    TRY
        Should be equal  1  1
    EXCEPT
        No Operation
    FINALLY
        No Operation
    END

TRY EXCEPT fail in EXCEPT
    TRY
        Should be equal  1  2
    EXCEPT
        Should be equal  1  2
    END

TRY FINALLY fail in FINALLY
    TRY
        No Operation
    FINALLY
        Should be equal  1  2
    END
