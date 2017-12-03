import os
import pandas as pd
import numpy as np
from pprint import pprint
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNet


class Pipeline(object):

    def __init__(self):
        pass

    def cleaning_data(self, df):
        # Dropping columns with 25% or more nulls
        # Dropping ID columns, duplicate columns, and meaningless columns
        # Dropping categorical columns with more than 100 unique values (too many for dummy variables)
        df.drop(
            ['MachineHoursCurrentMeter', 'UsageBand', 'fiSecondaryDesc', 'fiModelSeries', 'fiModelDescriptor', 'ProductSize',
             'Drive_System', 'Forks', 'Pad_Type', 'Ride_Control', 'Stick', 'Transmission', 'Turbocharged', 'Blade_Extension',
             'Blade_Width', 'Enclosure_Type', 'Engine_Horsepower', 'Pushblock', 'Ripper', 'Scarifier', 'Tip_Control', 'Tire_Size',
             'Coupler', 'Coupler_System', 'Grouser_Tracks', 'Hydraulics_Flow', 'Track_Type', 'Undercarriage_Pad_Width', 'Stick_Length',
             'Thumb', 'Pattern_Changer', 'Grouser_Type', 'Backhoe_Mounting', 'Blade_Type', 'Travel_Controls', 'Differential_Type', 'Steering_Controls',
             'SalesID', 'MachineID', 'ModelID', 'auctioneerID', 'ProductGroup', 'datasource', 'fiProductClassDesc', 'fiModelDesc', 'fiBaseModel'],
            axis=1, inplace=True)

        # Changing incorrect data types
        df['saledate'] = pd.to_datetime(df['saledate'])

        # Recoding none text and nonsense years into nulls
        df.replace('None or Unspecified', np.NaN, inplace=True)
        df['YearMade'].replace(1000, np.NaN, inplace=True)

        # Compute age column
        df['EquipmentAge'] = df['saledate'].dt.year - df['YearMade']
        df.drop('saledate', axis=1, inplace=True)

        # Create dummy variables
        df = pd.get_dummies(df, dummy_na=False)

        return df

    def modeling_prep(self, X_train, X_test, y_train):
        # Sorting X by types
        numerical_vals = X_train.select_dtypes(exclude=['object', 'bool', 'datetime'])

        # Fill null values with the mean from the training data
        for col in numerical_vals.columns:
            mean = X_train[col].mean()
            X_train[col].fillna(mean, inplace=True)
            X_test[col].fillna(mean, inplace=True)

        # Scaling data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train[numerical_vals.columns])
        X_train_scaled = np.concatenate(
            [X_train_scaled, X_train.drop(numerical_vals.columns, axis=1)], axis=1)

        # Scaling test data
        X_test_scaled = scaler.transform(X_test[numerical_vals.columns])
        X_test_scaled = np.concatenate(
            [X_test_scaled, X_test.drop(numerical_vals.columns, axis=1)], axis=1)

        return X_train_scaled, X_test_scaled, y_train, X_train

    def model_testing(self, X_train_scaled, y_train, X_train):
        # Selecting best features using recursive feature elimination
        model = ElasticNet()

        model = ElasticNet()
        param_list = {'alpha': np.linspace(0.6, 0.8, 20),
                      'l1_ratio': np.linspace(0.9, 1.0, 10)}

        # Grid searching hyperparameters
        g = GridSearchCV(model, param_list, scoring='neg_mean_squared_error',
                         cv=5, n_jobs=3, verbose=10)
        g.fit(X_train_scaled, y_train)
        results = g.cv_results_

        print('\n\n')
        pprint(results)
        print('\n\n')
        print('Best Params: {}, Best Score: {}'.format(g.best_params_, g.best_score_))

        # Print out regression coefficients
        coefs = list(g.best_estimator_.coef_)
        self.print_coefficients(X_train, coefs)

    def print_coefficients(self, X_train, coefs):
        '''
        Prints coefficients model in order of highest values
        '''
        # Creating a list of features
        features = list(X_train.columns)

        importances = []
        for x, y in zip(features, coefs):
            # Connecting features with their corresponding coefficients
            importances.append([x, y])

        # Sort coefficients in decreasing order of absolute values of the coefficients
        importances.sort(key=lambda row: abs(row[1]), reverse=True)
        # Cycling through the list to print for nicer formatting
        print('Coefficients:')
        for pair in importances:
            if pair[1] == 0.0:
                break
            else:
                print(pair)

    def final_model(self, X_train_scaled, X_test_scaled, y_train, X_train, test_df):
        # Best hyperparameter values from gridsearching results
        model = ElasticNet(alpha=0.71282051282051284, l1_ratio=0.97777777777777775)
        # Fitting model
        model.fit(X_train_scaled, y_train)
        y_test_predicted = model.predict(X_test_scaled)
        # coefs = list(model.coef_)
        # self.print_coefficients(X_train, coefs)
        test_df['SalePrice'] = y_test_predicted
        # Setting up the predictions to see how I did
        test_df[['SalesID', 'SalePrice']].to_csv('../data/output_data.csv', index=False)
        test_solution = pd.read_csv('../data/do_not_open/test_soln.csv')
        log_diff = np.log(y_test_predicted + 1) - np.log(test_solution['SalePrice'] + 1)
        score = np.sqrt(np.mean(log_diff**2))
        print('Final RMSLE Score: {}'.format(score))


if __name__ == '__main__':
    # Setting seed for reproducability
    np.random.seed(50)

    # Toggle to rerun data cleaning if changes are made
    rerun = False

    # Instantiate the class
    p = Pipeline()

    # Load the compressed data if it exists, otherwise clean the data and compress it
    if os.path.exists('../data/Xycompressed.npz') and rerun == False:
        npz = np.load('../data/Xycompressed.npz')
        X_train_scaled = npz['X_train_scaled']
        X_test_scaled = npz['X_test_scaled']
        y_train = npz['y_train']
        X_train = pd.read_pickle('../data/X_train')
        test_df = pd.read_csv('../data/test.csv', low_memory=False)
    else:
        train_df = pd.read_csv('../data/Train.csv', low_memory=False)
        # Shuffling the data
        train_df = train_df.iloc[np.random.permutation(train_df.shape[0])]
        test_df = pd.read_csv('../data/test.csv', low_memory=False)
        cutoff = len(train_df)
        # Temporarily combining training & test data to clean them both easier (espeically when making dummies)
        combined = pd.concat(objs=[train_df, test_df], axis=0)
        combined = p.cleaning_data(combined)
        # Splitting the training & testing data back up
        train_df = combined[:cutoff]
        X_test = combined[cutoff:]
        X_test.drop('SalePrice', axis=1, inplace=True)
        # Pulling out the target variable
        y_train = train_df.pop('SalePrice')
        X_train = train_df
        # Prepping the data for modeling purposes
        X_train_scaled, X_test_scaled, y_train, X_train = p.modeling_prep(
            X_train, X_test, y_train)
        # Compressing data for faster performance
        args = {'X_train_scaled': X_train_scaled,
                'X_test_scaled': X_test_scaled, 'y_train': y_train}
        np.savez_compressed('../data/Xycompressed', **args)
        X_train.to_pickle('../data/X_train')

    # Testing parameters
    # p.model_testing(X_train_scaled, y_train, X_train)

    # Running the final model
    p.final_model(X_train_scaled, X_test_scaled, y_train, X_train, test_df)
