# Quick and Simple Boolean Evaluator for 15-110 Grading

Make sure to follow the syntax invariants, there WILL be errors and the error messages will not be very helpful

The main thing is just how to run.
To run do either:
`python3 booleanEvaluator.py -e "<your expression>"`
`python3 booleanEvaluator.py --expression "<your expression>"`
Make sure the entire expression is placed within quotation marks.

### Limitations
Right now there are still quite a few limitations on what the input syntax must look like since under the hood there are a few syntax invariant assumptions to make the parsing logic a lot easier to implement.

Here are the main ones:
- The NOT gate only works on single inputs and not full expressions. ie. `NOT X` will work but `NOT (X AND Y)` will not work. The workaround is to just pull the logical NOT inside of the parentheses. ie. `NOT (X AND Y)` becomes `(NOT X) OR (NOT Y)`
- For two-input gates, full expressions on both sides or single inputs on both sides will work. However when operating on an expression and a single input the expression must be on the left hand side of the operator. ie. `(Y OR Z) AND X` will work but `X AND (Y OR Z)` will not work.
- Three-input gates are not yet implemented, so please use parentheses around operators. OR, XOR, and AND gates are all associative, so this is pretty easy. ie. `X AND Y AND Z` will not work so turn it into `(X AND Y) and Z`. Keep the expression and single input constraint from above in mind!!
- The NOT gate is implemented by overriding it with an XOR gate. ie. XOR-ing the input with a 1. So this could cause some bugs if the input expression is whack but doesn't throw off the parser.


The more exhaustive list of errors can be found at the top of the source file. Or you can just read the code to figure out the limitations :)

### Screenshot Examples
#### Things that work
![Working Example 1](https://github.com/WilliXL/boolean_evaluator/blob/master/screenshots/working1.png)
![Working Example 2](https://github.com/WilliXL/boolean_evaluator/blob/master/screenshots/working2.png)
![Working Example 3](https://github.com/WilliXL/boolean_evaluator/blob/master/screenshots/working3.png)
![Working Example 4](https://github.com/WilliXL/boolean_evaluator/blob/master/screenshots/working4.png)
![Working Example 4](https://github.com/WilliXL/boolean_evaluator/blob/master/screenshots/working5.png)

#### Things that DON'T work
![Singleton Input Variables Can't be on the Left](https://github.com/WilliXL/boolean_evaluator/blob/master/screenshots/not_working1.png)
![NOT Expression Isn't Working :(](https://github.com/WilliXL/boolean_evaluator/blob/master/screenshots/not_working3.png)
