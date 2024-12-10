import json

# GeoJSON 파일 경로
geojson_path = "./data/deajeun_yousounggu_dong.geojson"

# GeoJSON 데이터를 읽고 SVG 경로 생성
def geojson_to_svg_with_ids(geojson_data, scale=3000, offset_x=127.3, offset_y=36.4):
    """GeoJSON 데이터를 SVG 경로로 변환하고 각 path에 ID를 부여"""
    svg_paths = []
    for feature in geojson_data['features']:
        coordinates = feature['geometry']['coordinates']
        feature_id = feature['properties'].get('EMD_CD', 'unknown')  # ID로 사용할 필드
        feature_name = feature['properties'].get('EMD_KOR_NM', 'Unknown')  # 이름 필드

        # 멀티폴리곤 처리
        if feature['geometry']['type'] == 'Polygon':
            coordinates = [coordinates]

        for polygon in coordinates:
            path = "M "  # SVG 경로 시작
            for coord_pair in polygon[0]:  # 첫 번째 링
                x = (coord_pair[0] - offset_x) * scale
                y = -(coord_pair[1] - offset_y) * scale
                path += f"{x:.2f},{y:.2f} "
            path += "Z"  # 닫기
            svg_paths.append({
                'path': path.strip(),
                'id': feature_id,
                'name': feature_name
            })
    return svg_paths

# GeoJSON 파일 로드
with open(geojson_path, encoding='utf-8') as f:
    geojson_data = json.load(f)

# GeoJSON을 SVG 경로로 변환
svg_elements = geojson_to_svg_with_ids(geojson_data)

# SVG 및 HTML 생성
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>대전 유성구 지도</title>
    <style>
        svg {
            width: 100%;
            height: 100vh;
            background-color: #f0f0f0;
        }
        .dong {
            fill: lightblue;
            stroke: black;
            stroke-width: 0.5;
        }
        .dong:hover {
            fill: lightgreen;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <svg viewBox="0 0 1000 1000">
"""

# SVG 경로 추가
for element in svg_elements:
    path = element['path']
    path_id = element['id']
    path_name = element['name']
    html_content += f'        <path class="dong" id="{path_id}" d="{path}" onclick="alert(\'{path_name} 클릭됨\')"></path>\n'

html_content += """
    </svg>
</body>
</html>
"""

# HTML 파일 저장
output_file = "daejeon_yousounggu_dong_map.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"SVG 기반 HTML 파일이 생성되었습니다: {output_file}")