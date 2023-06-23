from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import os
from bs4 import BeautifulSoup
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
import random

RANDOM_STATE = 10

def testMLP(xt, xv, yt, yv, epochs=5000, learning_rate=0.001, hidden_sizes=(100,)):
    mlp = MLPRegressor(
        solver='sgd',
        alpha=0.0,
        learning_rate_init=learning_rate,
        random_state=RANDOM_STATE,
        hidden_layer_sizes=hidden_sizes
    )

    train_loss = []
    validation_loss = []

    for _ in range(epochs):
        mlp.partial_fit(xt, yt)

        pred_y_train = mlp.predict(xt)
        train_loss.append(mean_squared_error(y_train, pred_y_train))

        pred_y_validation = mlp.predict(X_validate)
        validation_loss.append(mean_squared_error(yv, pred_y_validation))

    return train_loss, validation_loss

def createPlots(xt, xv, yt, yv):
    learning_rates = [0.00001]
    hidden_sizes_list = [(100,), (200,), (100, 100,), (50,)]

    for lr in learning_rates:
        tl, vl = testMLP(xt, xv, yt, yv, learning_rate=lr, hidden_sizes=hidden_sizes_list[0])
        plt.plot(tl, label='Train loss')
        plt.plot(vl, label='Validation loss')
        plt.xlabel('epochs')
        plt.title(f"MLP learning_rate_init={lr} hidden_layer_sizes={hidden_sizes_list[0]}")
        plt.legend()
        plt.show()

    # for hs in hidden_sizes_list:
    #     tl, vl = testMLP(xt, xv, yt, yv, epochs=2000, learning_rate=learning_rates[0], hidden_sizes=hs)
    #     plt.plot(tl, label='Train loss')
    #     plt.plot(vl, label='Validation loss')
    #     plt.xlabel('epochs')
    #     plt.title(f"MLP learning_rate_init={learning_rates[0]} hidden_layer_sizes={hs}")
    #     plt.legend()
    #     plt.show()

def testMyJoke(X_train, X_validate, y_train, y_validate, jokes, joke=None):
    mlp = MLPRegressor(
        solver='sgd',
        alpha=0.0,
        learning_rate_init=0.00001,
        random_state=RANDOM_STATE
    )
    mlp.fit(X_train, y_train)
    mlp.score(X_validate, y_validate)

    if(joke is None):
        index = int(random.random() * len(jokes))
        myJoke = str(jokes[index])
    else:
        myJoke = joke
    print(myJoke)
    model = SentenceTransformer('bert-base-cased')
    embeddings = model.encode([myJoke])
    embeddings = np.reshape(embeddings, (1,-1))
    prediction = mlp.predict(embeddings)
    print(f"Predykcja -> {prediction}")



if __name__=="__main__":
    ratings = pd.read_excel("jester-data-1.xls", header=None)
    ratings = ratings.iloc[:, 1:].replace(99, float('nan'))

    avgRatings = ratings.mean()

    jokes = []

    jokesCount = len(os.listdir("jokes"))

    for i in range(1, jokesCount):
        with open(f"jokes/init{i}.html") as joke:
            joke_html = joke.read()
            soup = BeautifulSoup(joke_html, 'html.parser')
            joke_text = soup.find('font', size='+1').text.strip()
            jokes.append(joke_text)

    model = SentenceTransformer('bert-base-cased')
    embeddings = model.encode(jokes)

    X_train, X_validate, y_train, y_validate = train_test_split(
        embeddings, 
        avgRatings, 
        test_size=0.2, 
        random_state=RANDOM_STATE
    )

    # createPlots(X_train, X_validate, y_train, y_validate)

    testMyJoke(X_train, X_validate, y_train, y_validate, jokes, joke="Co jest męczące, któtkie i zabiera cały piątek?\n\nKolokwium z Rozproszonych Systemów Informatycznych")
    testMyJoke(X_train, X_validate, y_train, y_validate, jokes)

