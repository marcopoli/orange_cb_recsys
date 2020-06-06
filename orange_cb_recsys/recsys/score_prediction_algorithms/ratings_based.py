import os
import pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn import tree

from orange_cb_recsys.content_analyzer.content_representation.content import Content
from orange_cb_recsys.recsys.score_prediction_algorithms.score_prediction_algorithm import RatingsSPA

import pandas as pd


class CentroidVector(RatingsSPA):
    def __init__(self, item_field: str, field_representation: str):
        super().__init__(item_field, field_representation)

    def predict(self, item: Content, ratings: pd.DataFrame, items_directory: str):
        """
        1) Goes into items_directory and for each item takes the values corresponding to the field_representation
        of the item_field. For example, if item_field == "Plot" and field_representation == "Document embedding",
        the function will take the "Document embedding" representation of each  "Plot" field for every item;
        2) Computes the weighted centroid between the representations. In order to do that, field_representation must
        be a representation that allows the computation of a centroid, otherwise the method will raise an exception;
        3) Determines the similarity between the centroid and the field_representation of the item_field in item.

        Args:
            item (Content): Item for which the similarity will be computed
            ratings (pd.DataFrame): Ratings
            items_directory (str): Name of the directory where the items are stored.

        Returns:
             ----- similarity (float): The similarity between the item and the other items
        """
        return 5.0


class ClassifierRecommender(RatingsSPA):
    """
       Class that implements a decisiontreeclassifier.
       Args:
           item_field (str): Name of the field that contains the content to use
           field_representation (str): Id of the field_representation content
       """
    def __init__(self, item_field: str, field_representation: str):
        super().__init__(item_field, field_representation)

    def predict(self, item: Content, ratings: pd.DataFrame, items_directory: str):
        """
        1) Goes into items_directory and for each item takes the values corresponding to the field_representation of
        the item_field. For example, if item_field == "Plot" and field_representation == "tf-idf", the function will
        take the "tf-idf" representation of each  "Plot" field for every item;
        2) Takes a list of ratings that are in the dataframe (rated_item_index_list) and does a trasformation on that
        list with the dictvectorizer;
        3) Creates an object DecisionTreeClassifier, uses the method fit and predicts the class of the item

                Args:
                    item (Content): Item for which the similarity will be computed
                    ratings (pd.DataFrame): Ratings
                    items_directory (str): Name of the directory where the items are stored.

                Returns:
                     The predicted classes, or the predict values.
                """
        items = [filename for filename in os.listdir(items_directory)]

        features_bag_list = []
        rated_item_index_list = []
        for item in items:
            item_filename = items_directory + '/' + item
            with open(item_filename, "rb") as content_file:
                content = pickle.load(content_file)

                features_bag_list.append(content.get_field("Plot").get_representation("1").get_value())
        features_bag_list.append(content.get_field("Plot").get_representation("1").get_value())
        v = DictVectorizer(sparse=False)

        for i in features_bag_list:
            if features_bag_list[i].get_content_id() in ratings.item_id:
                rated_item_index_list.append(features_bag_list[i])

        X_tmp = v.fit_transform(rated_item_index_list)

        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X_tmp, ratings.score)

        return clf.predict(item)
