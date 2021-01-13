from flask import Flask, render_template, request

from preprocessing.web_app_builder import WebAppBuilder, WebAppPredictionHolder, ModelPrediction, get_user_id_from_user

app = Flask(__name__)

web_app_builder = WebAppBuilder()
products = web_app_builder.get_products_for_web()
users = web_app_builder.get_users_for_web()
prediction_holder = WebAppPredictionHolder()


@app.route('/')
def discount_service():
    return render_template('index.html', users=users, products=products)


@app.route('/first_model_discount', methods=['POST'])
def first_model_discount():
    user = request.form.get('user_id')
    user_id = get_user_id_from_user(user)
    product = request.form.get('product')
    # TODO: tutaj trzeba uzupelnic predykcje drugiego modelu
    discount = ' '
    prediction_holder.first_model = ModelPrediction([user, product, discount])
    return render_app()


@app.route('/second_model_discount', methods=['POST'])
def second_model_discount():
    user = request.form.get('user_id')
    user_id = get_user_id_from_user(user)
    product = request.form.get('product')
    # TODO: tutaj trzeba uzupelnic predykcje drugiego modelu
    discount = ' '
    prediction_holder.second_model = ModelPrediction([user, product, discount])
    return render_app()


def render_app():
    return render_template('index.html', users=users, products=products,
                           first_model_discount=prediction_holder.first_model.prediction,
                           second_model_discount=prediction_holder.second_model.prediction)


if __name__ == '__main__':
    app.run()
