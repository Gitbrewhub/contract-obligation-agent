from datetime import datetime
from pathlib import Path
import traceback

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

from database.retrieval import get_obligations_by_contract
from graph.workflow import build_contract_graph


# =========================================================
# CONFIGURATION
# =========================================================

UPLOAD_FOLDER = Path("contracts/uploads")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
}


# =========================================================
# HELPERS
# =========================================================

def allowed_file(filename: str) -> bool:
    """
    Check whether the uploaded file has a supported extension.
    """
    if not filename:
        return False

    extension = Path(filename).suffix.lower()

    return extension in ALLOWED_EXTENSIONS


# =========================================================
# CREATE FLASK APP
# =========================================================

def create_app():

    app = Flask(__name__)

    # -----------------------------------------------------
    # CORS
    # -----------------------------------------------------
    #
    # React/Vite normally runs on:
    #
    #   http://localhost:5173
    #
    # or:
    #
    #   http://127.0.0.1:5173
    #
    # Flask runs on:
    #
    #   http://127.0.0.1:5000
    #
    # These are different origins, so the browser needs
    # permission to communicate with Flask.
    #
    # -----------------------------------------------------

    CORS(
        app,
        resources={
            r"/contracts/*": {
                "origins": [
                    "http://localhost:5173",
                    "http://127.0.0.1:5173",
                ]
            },
            r"/health": {
                "origins": [
                    "http://localhost:5173",
                    "http://127.0.0.1:5173",
                ]
            },
        },
    )

    # -----------------------------------------------------
    # Upload configuration
    # -----------------------------------------------------

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    UPLOAD_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -----------------------------------------------------
    # Build LangGraph workflow once when Flask starts
    # -----------------------------------------------------

    print()
    print("=" * 80)
    print("INITIALIZING CONTRACT.AI BACKEND")
    print("=" * 80)

    try:
        contract_graph = build_contract_graph()

        print("LangGraph workflow initialized successfully.")

    except Exception as exc:

        print()
        print("=" * 80)
        print("LANGGRAPH INITIALIZATION ERROR")
        print("=" * 80)

        print(
            f"Exception type: {type(exc).__name__}"
        )

        print(
            f"Exception message: {exc}"
        )

        traceback.print_exc()

        print("=" * 80)
        print()

        raise

    print("=" * 80)
    print()


    # =====================================================
    # HEALTH CHECK
    # =====================================================

    @app.get("/health")
    def health():

        return jsonify(
            {
                "status": "ok",
                "service": "contract-obligation-agent",
                "orchestration": "langgraph",
            }
        )


    # =====================================================
    # GET CONTRACT OBLIGATIONS
    # =====================================================

    @app.get(
        "/contracts/<int:contract_id>/obligations"
    )
    def get_contract_obligations(contract_id):

        try:

            obligations = (
                get_obligations_by_contract(
                    contract_id
                )
            )

            return jsonify(
                {
                    "contract_id": contract_id,
                    "count": len(obligations),
                    "obligations": obligations,
                }
            )

        except Exception as exc:

            print()
            print("=" * 80)
            print("DATABASE RETRIEVAL ERROR")
            print("=" * 80)

            print(
                f"Contract ID: {contract_id}"
            )

            print(
                f"Exception type: {type(exc).__name__}"
            )

            print(
                f"Exception message: {exc}"
            )

            traceback.print_exc()

            print("=" * 80)
            print()

            return jsonify(
                {
                    "error": "Unable to retrieve obligations",
                    "details": str(exc),
                    "exception_type": type(exc).__name__,
                }
            ), 500


    # =====================================================
    # UPLOAD + ANALYZE CONTRACT
    # =====================================================

    @app.post("/contracts/upload")
    def upload_contract():

        print()
        print("=" * 80)
        print("UPLOAD REQUEST RECEIVED")
        print("=" * 80)

        # -------------------------------------------------
        # Check file
        # -------------------------------------------------

        if "file" not in request.files:

            print(
                "ERROR: No file field found in request."
            )

            return jsonify(
                {
                    "error": "No file was uploaded."
                }
            ), 400

        uploaded_file = request.files["file"]

        # -------------------------------------------------
        # Check filename
        # -------------------------------------------------

        if not uploaded_file.filename:

            print(
                "ERROR: Uploaded file has no filename."
            )

            return jsonify(
                {
                    "error": "No filename was provided."
                }
            ), 400

        original_filename = uploaded_file.filename

        filename = secure_filename(
            original_filename
        )

        print(
            f"Original filename: {original_filename}"
        )

        print(
            f"Secure filename: {filename}"
        )

        # -------------------------------------------------
        # Check extension
        # -------------------------------------------------

        if not allowed_file(filename):

            print(
                "ERROR: Unsupported file type."
            )

            return jsonify(
                {
                    "error": (
                        "Unsupported file type. "
                        "Only PDF and DOCX files are supported."
                    )
                }
            ), 400

        # -------------------------------------------------
        # Save uploaded file
        # -------------------------------------------------

        upload_path = (
            UPLOAD_FOLDER / filename
        )

        print(
            f"Saving uploaded file: {upload_path}"
        )

        try:

            uploaded_file.save(
                upload_path
            )

            print(
                "File saved successfully."
            )

        except Exception as exc:

            print()
            print("=" * 80)
            print("FILE SAVE ERROR")
            print("=" * 80)

            print(
                f"Exception type: {type(exc).__name__}"
            )

            print(
                f"Exception message: {exc}"
            )

            traceback.print_exc()

            print("=" * 80)
            print()

            return jsonify(
                {
                    "error": "Unable to save uploaded file.",
                    "details": str(exc),
                    "exception_type": type(exc).__name__,
                }
            ), 500

        # -------------------------------------------------
        # Run LangGraph
        # -------------------------------------------------

        print(
            "Starting LangGraph contract processing..."
        )

        try:

            result = contract_graph.invoke(
                {
                    "file_path": str(
                        upload_path
                    ),
                    "reference_date": datetime.now(),
                }
            )

            print(
                "LangGraph processing completed."
            )

        except Exception as exc:

            print()
            print("=" * 80)
            print("CONTRACT PROCESSING ERROR")
            print("=" * 80)

            print(
                f"Exception type: {type(exc).__name__}"
            )

            print(
                f"Exception message: {exc}"
            )

            print("-" * 80)

            traceback.print_exc()

            print("=" * 80)
            print()

            return jsonify(
                {
                    "error": "Contract processing failed",
                    "details": str(exc),
                    "exception_type": type(exc).__name__,
                }
            ), 500

        # -------------------------------------------------
        # Extract LangGraph result
        # -------------------------------------------------

        results = result.get(
            "results",
            []
        )

        contract_id = result.get(
            "contract_id"
        )

        print(
            f"Contract ID: {contract_id}"
        )

        print(
            f"Obligations found: {len(results)}"
        )

        # -------------------------------------------------
        # Safety check
        # -------------------------------------------------

        if contract_id is None:

            print(
                "ERROR: LangGraph completed but "
                "did not return contract_id."
            )

            return jsonify(
                {
                    "error": (
                        "Contract processing completed "
                        "but no contract ID was returned."
                    )
                }
            ), 500

        # -------------------------------------------------
        # Successful response
        # -------------------------------------------------

        response_data = {
            "contract_id": contract_id,
            "filename": filename,
            "count": len(results),
            "orchestration": "langgraph",
            "obligations": results,
        }

        print(
            "Upload request completed successfully."
        )

        print("=" * 80)
        print()

        return jsonify(
            response_data
        ), 201


    # =====================================================
    # RETURN APP
    # =====================================================

    return app


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

app = create_app()


if __name__ == "__main__":

    print()
    print("=" * 80)
    print("CONTRACT.AI FLASK SERVER")
    print("=" * 80)
    print("Backend: http://127.0.0.1:5000")
    print("Health:  http://127.0.0.1:5000/health")
    print("=" * 80)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False,
    )