import folium
import json

# 대전 중심 좌표 설정
daejeon_center = [36.3504, 127.3845]

# 지도 생성
map_daejeon = folium.Map(location=daejeon_center, zoom_start=12)

# GeoJSON 파일 경로들
gu_geojson_path = './data/deajeun_gu.geojson'
dong_geojson_files = {
    "유성구": "./data/deajeun_yousounggu_dong.geojson",
    "서구": "./data/deajeun_sugu_dong.geojson",
    "대덕구": "./data/deajeun_daduckgu_dong.geojson",
    "중구": "./data/deajeun_joonggu_dong.geojson",
    "동구": "./data/deajeun_donggu_dong.geojson",
}

# 대전의 구 GeoJSON 로드
with open(gu_geojson_path, encoding='utf-8') as f:
    daejeon_geojson = json.load(f)


# 구 스타일 지정
def gu_style_function(feature):
    """구 스타일"""
    return {
        'fillColor': 'blue',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5,
    }


# 구 GeoJSON 데이터를 지도에 추가
for feature in daejeon_geojson['features']:
    gu_name = feature['properties'].get('SIG_KOR_NM', 'Unknown')  # 필드 이름 수정

    # 각 구의 동 GeoJSON 로드
    dong_geojson_path = dong_geojson_files.get(gu_name)
    if dong_geojson_path:
        with open(dong_geojson_path, encoding='utf-8') as f:
            dong_geojson = json.load(f)

        # 동 데이터를 클릭 이벤트로 연결
        dong_layer = folium.FeatureGroup(name=f"{gu_name} 동")
        folium.GeoJson(
            dong_geojson,
            style_function=lambda x: {
                'fillColor': 'green',
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.4,
            },
            tooltip=folium.GeoJsonTooltip(fields=['EMD_KOR_NM'], aliases=['동:']),  # 필드 이름 수정
        ).add_to(dong_layer)
        dong_layer.add_to(map_daejeon)

    # 구를 지도에 추가
    folium.GeoJson(
        feature,
        style_function=gu_style_function,
        tooltip=folium.GeoJsonTooltip(fields=['SIG_KOR_NM'], aliases=['구:']),  # 필드 이름 수정
    ).add_to(map_daejeon)

# 레이어 컨트롤 추가
folium.LayerControl().add_to(map_daejeon)

# HTML 파일로 저장
map_daejeon.save("daejeon_gu_dong_map.html")
print("HTML 지도 파일이 생성되었습니다: daejeon_gu_dong_map.html")