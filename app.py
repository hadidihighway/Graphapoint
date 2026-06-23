from flask import Flask, render_template, request, redirect, url_for, jsonify
import Graphapoint

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/api/plot', methods=['GET', 'POST'])
def api_plot():
    
    if request.method == 'POST':
        data = request.get_json() or request.form
        x = data.get('x')
        y = data.get('y')
    else:
        x = request.args.get('x')
        y = request.args.get('y')

    try:
        x = int(x)
        y = int(y)
    except Exception:
        return jsonify({'error': 'Invalid or missing x,y parameters'}), 400

    point = (x, y)
    width = Graphapoint.DEFAULT_WIDTH
    height = Graphapoint.DEFAULT_HEIGHT
    spacing = Graphapoint.DEFAULT_SPACING

    
    x1, y1, x2, y2 = Graphapoint.line_endpoints(point, width=width, spacing=spacing)
    cpx, cpy = Graphapoint.to_canvas(x, y, width=width, height=height, spacing=spacing)
    c1x, c1y = Graphapoint.to_canvas(x1, y1, width=width, height=height, spacing=spacing)
    c2x, c2y = Graphapoint.to_canvas(x2, y2, width=width, height=height, spacing=spacing)

    return jsonify({
        'point': {'x': x, 'y': y},
        'canvas_point': {'x': cpx, 'y': cpy},
        'line': [{'x': c1x, 'y': c1y}, {'x': c2x, 'y': c2y}],
        'width': width,
        'height': height,
        'spacing': spacing,
    })


if __name__ == '__main__':
    app.run(debug=True)
