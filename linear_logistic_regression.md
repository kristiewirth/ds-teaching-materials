* Homoscedasticity means “having the same scatter.” For it to exist in a set of data, the points must be about the same distance from the line.
* The opposite is heteroscedasticity (“different scatter”), where points are at widely varying distances from the regression line.


* Lasso penalties are better at recovering sparse signals.
* Ridge penalties are better at minimizing prediction error.


* Logit odds - What you get when you run a logistic regression in sklearn. Great for comparing apples to apples, i.e. standardizing units.
* Odds - These are the actual odds. So you can say things like, “Customers in retail are 56 times more likely to buy product x”. To get them --> e^logit_odds
* Probability - So you can say things like, “The probability of a customer in retail buying product  x is _ %“. To get them --> odds / (1 + odds)


* Linear regression: If you increase X by 1 unit, y is predicted to increase by the given coefficient value (B1) respectively if the other features are held constant.
* Logistic regression: If you increase X by 1 unit, the log odds increases by the given coefficient value (B1) respectively if the other features are held constant.

# Log odds to odds
```odds = np.exp(results.params)```
Interpretation: If you increase X by 1, the odds of y increases by the [given odds number].

# Log odds to probability
```probs = sp.special.expit(results.params['intercept'] + results.params['X'])```
Interpretation: Given that X = 1, the probability of y is [given probability number].
