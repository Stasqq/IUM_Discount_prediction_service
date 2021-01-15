from flask import Flask, render_template, request

from preprocessing.web_app_builder import WebAppBuilder, WebAppPredictionHolder, ModelPrediction, get_user_id_from_user, \
    get_product_id_from_product

app = Flask(__name__)

web_app_builder = WebAppBuilder()
products = web_app_builder.get_products_for_web()
users = web_app_builder.get_users_for_web()


@app.route('/')
def discount_service():
    return render_app()


@app.route('/first_model_discount', methods=['POST'])
def first_model_discount():
    web_app_builder.predict_with_first_model(request.form.get('user_id'), request.form.get('product'))
    return render_app()


@app.route('/second_model_discount', methods=['POST'])
def second_model_discount():
    web_app_builder.predict_with_second_model(request.form.get('user_id'), request.form.get('product'),)
    return render_app()


def render_app():
    return render_template('index.html', users=users, products=products,
                           first_model_discount=web_app_builder.prediction_holder.first_model.prediction,
                           second_model_discount=web_app_builder.prediction_holder.second_model.prediction)


if __name__ == '__main__':
    app.run()
