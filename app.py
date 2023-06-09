import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

@st.cache_data
def load_data():
    data = pd.read_csv('bus_stop.csv')
    data = data.rename(columns={'위도': 'latitude', '경도': 'longitude'})
    return data

data = load_data()

st.title('대한민국 버스 정류장 정보 조회')
st.markdown('버스정보시스템(BIS)이 구축된 지자체 중 국가대중교통정보센터(TAGO)와 연계된 139개 지자체의 버스정류장 위치정보 데이터입니다.')

city_to_search = st.selectbox("정류장명을 검색할 도시를 선택하세요.", data['도시명'].unique())
bus_stop_to_search = st.selectbox("정류장명을 선택하세요.", data[data['도시명'] == city_to_search]['정류장명'].unique())
if bus_stop_to_search:
    bus_stop_data = data[(data['정류장명'] == bus_stop_to_search) & (data['도시명'] == city_to_search)]
    st.write(bus_stop_data)
    st.map(bus_stop_data)  # 버스 정류장을 지도에 표시


if st.checkbox('정류장 간 거리를 계산하시겠습니까?'):
    # 배열로 반환
    city_to_calculate_1 = st.selectbox("첫 번째 도시를 선택하세요.", data['도시명'].unique())
    # 선택된 도시의 정류장 표시
    bus_stop_1 = st.selectbox('첫 번째 도시의 정류장을 선택하세요.', data[data['도시명'] == city_to_calculate_1]['정류장명'].unique())
    
    city_to_calculate_2 = st.selectbox("두 번째 도시를 선택하세요.", data['도시명'].unique())
    bus_stop_2 = st.selectbox('두 번째 도시의 정류장을 선택하세요.', data[data['도시명'] == city_to_calculate_2]['정류장명'].unique())

    location_1 = data[(data['정류장명'] == bus_stop_1) & (data['도시명'] == city_to_calculate_1)][['longitude', 'latitude']].values[0]
    location_2 = data[(data['정류장명'] == bus_stop_2) & (data['도시명'] == city_to_calculate_2)][['longitude', 'latitude']].values[0]
    
    # loocation_1,2 : 경도(longitude), 위도(latitude) 값을 가지며,두 개의 지점 객체를 생성
    gdf = gpd.GeoDataFrame(geometry=[Point(location_1[0], location_1[1]), Point(location_2[0], location_2[1])])
    # 좌표 참조 시스템
    gdf = gdf.set_crs('EPSG:4326')
    gdf = gdf.to_crs('EPSG:3857') 
    distance = gdf.geometry.distance(gdf.shift()).values[1] / 1000  

    st.write(f"{city_to_calculate_1}의 {bus_stop_1}과(와) {city_to_calculate_2}의 {bus_stop_2} 사이의 거리는 {distance:.2f} km 입니다.")

if st.checkbox('도시별 정류장 수를 보시겠습니까?'):
    selected_cities = st.multiselect('도시를 선택하세요.', data['도시명'].unique())
    if selected_cities:
        city_counts = data[data['도시명'].isin(selected_cities)]['도시명'].value_counts()
        st.bar_chart(city_counts)


st.image('bus_image.png')
