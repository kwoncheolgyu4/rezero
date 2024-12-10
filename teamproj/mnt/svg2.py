import json

# GeoJSON 경로
geojson_path = "./data/deajeun_donggu_dong.geojson"

# 좌표 범위 계산 함수
def calculate_bounds(geojson_data):
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    for feature in geojson_data['features']:
        coordinates = feature['geometry']['coordinates']
        if feature['geometry']['type'] == 'Polygon':
            coordinates = [coordinates]
        for polygon in coordinates:
            for coord_pair in polygon[0]:
                x, y = coord_pair
                min_x, max_x = min(min_x, x), max(max_x, x)
                min_y, max_y = min(min_y, y), max(max_y, y)
    return min_x, max_x, min_y, max_y

# GeoJSON 데이터 로드
with open(geojson_path, encoding='utf-8') as f:
    geojson_data = json.load(f)

# 좌표 범위 계산
min_x, max_x, min_y, max_y = calculate_bounds(geojson_data)

# 오프셋 및 스케일 계산
offset_x = (min_x + max_x) / 2
offset_y = (min_y + max_y) / 2
scale = min(1000 / (max_x - min_x), 1000 / (max_y - min_y))

# GeoJSON을 SVG 경로로 변환
def geojson_to_svg_with_ids(geojson_data, scale, offset_x, offset_y):
    svg_paths = []
    for feature in geojson_data['features']:
        coordinates = feature['geometry']['coordinates']
        feature_id = feature['properties'].get('EMD_CD', 'unknown')
        feature_name = feature['properties'].get('EMD_KOR_NM', 'Unknown')
        if feature['geometry']['type'] == 'Polygon':
            coordinates = [coordinates]
        for polygon in coordinates:
            path = "M "
            for coord_pair in polygon[0]:
                x = (coord_pair[0] - offset_x) * scale
                y = -(coord_pair[1] - offset_y) * scale
                path += f"{x:.2f},{y:.2f} "
            path += "Z"
            svg_paths.append({
                'path': path.strip(),
                'id': feature_id,
                'name': feature_name
            })
    return svg_paths

svg_elements = geojson_to_svg_with_ids(geojson_data, scale, offset_x, offset_y)

# SVG 생성
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지도</title>
    <style>
        svg {{ width: 100%; height: 100vh; background-color: #f0f0f0; }}
        .dong {{ fill: lightblue; stroke: black; stroke-width: 0.5; }}
        .dong:hover {{ fill: lightgreen; cursor: pointer; }}
    </style>
</head>
<body>
    <svg viewBox="{-500} {-500} {1000} {1000}">
"""

for element in svg_elements:
    path = element['path']
    path_id = element['id']
    path_name = element['name']
    html_content += f'<path class="dong" id="{path_id}" name="{path_name}" d="{path}" onclick="alert(\'{path_name} 클릭됨\')"></path>\n'

html_content += """
    </svg>
</body>
</html>
"""

# HTML 저장
with open("daejeon_map_dong.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML 파일이 생성되었습니다: daejeon_map_adjusted.html")