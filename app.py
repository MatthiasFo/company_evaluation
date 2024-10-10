from flask import Flask, jsonify
from src.adapters.logger import setup_logging_for_cloud_and_local
from src.use_cases.fetch_new_yahoo_company_data import (
    YahoooScraperUseCase,
)
from src.use_cases.fetch_alphavantage_company_data import (
    AlphavantageScraperUseCase,
)
from src.use_cases.evaluate_companies import CompanyEvaluation
from src.use_cases.fetch_fmp_company_data import FmpScraperUseCase


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)

    setup_logging_for_cloud_and_local()

    @app.route("/ping", methods=["GET"])
    def ping():
        print("Received a ping")
        return jsonify({"message": "pong"}), 200

    @app.route("/fetch-new-yahoo-data", methods=["GET"])
    def fetch_new_stocks_from_yahoo():
        result = YahoooScraperUseCase().fetch_yahoo_company_data()
        print(result["message"])
        if result["success"]:
            return jsonify({"message": result["message"]}), 200
        return jsonify({"message": result["message"]}), 500

    @app.route("/evaluate-companies", methods=["GET"])
    def run_company_evaluation():
        result = CompanyEvaluation().evaluate_companies()
        print(result["message"])
        if result["success"]:
            return jsonify({"message": result["message"]}), 200
        return jsonify({"message": result["message"]}), 500

    @app.route("/fetch-new-fmp-data", methods=["GET"])
    def fetch_new_stocks_from_fmp():
        result = FmpScraperUseCase().fetch_fmp_company_data()
        print(result["message"])
        if result["success"]:
            return jsonify({"message": result["message"]}), 200
        return jsonify({"message": result["message"]}), 500

    @app.route("/fetch-new-alphavantage-data", methods=["GET"])
    def fetch_new_stocks_from_alphavantage():
        result = AlphavantageScraperUseCase().fetch_alphavantage_company_data()
        print(result["message"])
        if result["success"]:
            return jsonify({"message": result["message"]}), 200
        return jsonify({"message": result["message"]}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
