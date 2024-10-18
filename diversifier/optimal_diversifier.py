from scipy.optimize import minimize
import numpy as np

class OptimalDiversifier(object):
    
    def __init__(self):
        self.name = "optimal_diversifier"

    def diversify(self, todays_sim, index, number_of_positions):
        # Get the return column and risk (market covariance)
        return_col = [col for col in todays_sim.columns if "return" in col][0]
        returns = todays_sim[return_col]
        risk = todays_sim["risk"]

        # Precompute the covariance matrix (diagonal only, for simplicity)
        cov_matrix = np.diag(risk)

        # Initial guess for weights (equal distribution)
        initial_guess = np.ones(len(returns)) / len(returns)

        # Bounds for weights
        bounds = [(0, 1) for _ in range(len(returns))]

        # Constraint: sum of weights must equal 1 (fully invested)
        constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}

        # Optimization using L-BFGS-B for speed
        result = minimize(self.portfolio_variance, initial_guess, args=(cov_matrix,), 
                          method='L-BFGS-B', bounds=bounds, constraints=constraints, 
                          options={'disp': False})  # 'disp': False for no console output

        # Check if optimization was successful
        if not result.success:
            raise ValueError(f"Optimization failed: {result.message}")

        # Optimized portfolio weights
        optimal_weights = result.x

        # Assign weights to todays_sim and filter non-zero weights
        todays_sim["weight"] = optimal_weights
        return todays_sim[todays_sim["weight"] > 0]

    # Portfolio variance: fully vectorized
    def portfolio_variance(self, weights, cov_matrix):
        return weights.T @ cov_matrix @ weights
