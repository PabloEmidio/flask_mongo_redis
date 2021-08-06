from flask import Flask, jsonify

def init_app(app: Flask):

    @app.errorhandler(404)
    def not_found(error):
        message_error = {
            'message': 'content not fount',
            'status_code': 404
        }
        return (
            jsonify(message_error),
            message_error['status_code']
        )
    
    @app.errorhandler(500)
    def not_found(error):
        message_error = {
            'message': str(error),
            'status_code': 500
        }
        return (
            jsonify(message_error),
            message_error['status_code']
        )