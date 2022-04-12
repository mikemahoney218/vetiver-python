from ..ptype import _vetiver_create_ptype
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

import pandas as pd
=======
=======
>>>>>>> e94bfec (adding tests)
from ..meta import vetiver_meta
import sklearn
>>>>>>> 1874222 (handle loading requirements for docker)
import numpy as np
<<<<<<< HEAD
=======
from ..meta import vetiver_meta

>>>>>>> 9979f1c (handle loading requirements for docker)
=======
>>>>>>> e94bfec (adding tests)

class SKLearnHandler:
    """Handler class for creating VetiverModels with sklearn.

    Parameters
    ----------
    model : sklearn.base.BaseEstimator
        a trained sklearn model
    """

    def __init__(self, model, ptype_data, save_ptype):
        self.model = model
        self.ptype_data = ptype_data
        self.save_ptype = save_ptype

    def create_description(self):
        """Create description for sklearn model"""
        desc = f"Scikit-learn model of type {type(self.model)}"
        return desc

    def vetiver_create_meta(
        user: list = None,
        version: str = None,
        url: str = None,
        required_pkgs: list = [],
    ):
        """Create metadata for sklearn model"""
<<<<<<< HEAD
<<<<<<< HEAD
        required_pkgs = required_pkgs + ["scikit-learn"]
=======
        required_pkgs = required_pkgs + ["torch"]
>>>>>>> 9979f1c (handle loading requirements for docker)
=======
        required_pkgs = required_pkgs + ["scikit-learn"]
>>>>>>> 361d192 (use pins read/write)
        meta = vetiver_meta(user, version, url, required_pkgs)

        return meta

    def ptype(self):
        """Create data prototype for torch model

        Parameters
        ----------
        ptype_data : pd.DataFrame, np.ndarray, or None
            Training data to create ptype
        save_ptype : bool

        Returns
        -------
        ptype : pd.DataFrame or None
            Zero-row DataFrame for storing data types
        """
        ptype = _vetiver_create_ptype(self.ptype_data, self.save_ptype)
        return ptype

    def handler_startup():
        """Include required packages for prediction

        The `handler_startup` function executes when the API starts. Use this
        function for tasks like loading packages.
        """
        ...


    def handler_predict(self, input_data, check_ptype):
        """Generates method for /predict endpoint in VetiverAPI

        The `handler_predict` function executes at each API call. Use this
        function for calling `predict()` and any other tasks that must be executed
        at each API call.

        Parameters
        ----------
        input_data:
            Test data

        Returns
        -------
        prediction
            Prediction from model
        """
        if check_ptype == True:
<<<<<<< HEAD
            if isinstance(input_data, pd.DataFrame):
                prediction = self.model.predict(input_data)
            else:
               prediction = self.model.predict([input_data])
=======
        ...

    def handler_predict(self, input_data, predict_proba: bool = False):
        import sklearn
>>>>>>> 9979f1c (handle loading requirements for docker)

        # do not check ptype
        else:
            if not isinstance(input_data, list):
                input_data = [input_data.split(",")]  # user delimiter ?

            prediction = self.model.predict(input_data)
=======
            prediction = self.model.predict([input_data])
        else:
            input_data = input_data.split(",")  # user delimiter ?
            input_data = np.asarray(input_data)
            reshape_data = input_data.reshape(1, -1)
            prediction = self.model.predict(reshape_data)
>>>>>>> e94bfec (adding tests)

        return prediction
