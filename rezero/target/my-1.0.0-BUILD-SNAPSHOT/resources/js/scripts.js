

document.addEventListener("DOMContentLoaded", () => {
    const rectangles = document.querySelectorAll(".Rectangle-9");
    const button1 = document.getElementById("button1"); // 첫 번째 버튼
    const button2 = document.getElementById("button2"); // 두 번째 버튼
    const tableHeader = document.querySelector(".thst.grid2 th:last-child");

    rectangles.forEach((rect) => {
        rect.addEventListener("click", () => {
            // 모든 네모를 inactive로 설정
            rectangles.forEach((r) => {
                r.classList.remove("active");
                const textSpan = r.querySelector("span");
                if (textSpan) {
                    textSpan.classList.remove("active-text");
                    textSpan.classList.add("inactive-text");
                }
            });

            // 클릭된 네모를 active로 설정
            rect.classList.add("active");
            const activeTextSpan = rect.querySelector("span");
            if (activeTextSpan) {
                activeTextSpan.classList.remove("inactive-text");
                activeTextSpan.classList.add("active-text");
            }
        });
    });

    // 기본 선택값
    rectangles[0].classList.add("active");
    const defaultTextSpan = rectangles[0].querySelector("span");
    if (defaultTextSpan) {
        defaultTextSpan.classList.remove("inactive-text");
        defaultTextSpan.classList.add("active-text");
    }

    // 버튼 초기 상태 설정
    button1.classList.add("active");

    // 버튼 클릭 이벤트 핸들러 추가
    button1.addEventListener("click", () => {
        setActiveButton(button1, button2);
        updateTableHeader(); // 테이블 헤더 업데이트
    });

    button2.addEventListener("click", () => {
        setActiveButton(button2, button1);
        updateTableHeader(); // 테이블 헤더 업데이트
    });

    function setActiveButton(activeButton, inactiveButton) {
        // 활성화된 버튼 스타일 설정
        activeButton.classList.add("active");
        // 비활성화된 버튼 스타일 제거
        inactiveButton.classList.remove("active");
    }
    
    // 테이블 헤더 업데이트 함수
    function updateTableHeader() {
        const isEnergyUsage = document.getElementById("slider-button").style.left === "0px" || document.getElementById("slider-button").style.left === "";
        const isElectric = document.getElementById("button1").classList.contains("active");
        
        if (isEnergyUsage) {
            // 에너지 사용량 모드
            if (isElectric) {
                tableHeader.innerHTML = "전기 에너지 사용량<br>(MWh)";
            } else {
                tableHeader.innerHTML = "가스 에너지 사용량<br>(천m³)";
            }
        } else {
            // 온실가스 배출량 모드
            if (isElectric) {
                tableHeader.innerHTML = "전기 온실가스 배출량<br>(tCO₂)";
            } else {
                tableHeader.innerHTML = "가스 온실가스 배출량<br>(tCO₂)";
            }
        }
    }
});

function toggleSlider() {
    const sliderButton = document.getElementById("slider-button");
    const sliderTextLeft = document.querySelector(".slider-text-left");
    const sliderTextRight = document.querySelector(".slider-text-right");
    const button1 = document.getElementById("button1"); // 첫 번째 버튼
    const button2 = document.getElementById("button2"); // 두 번째 버튼
    // 테이블 헤더 요소 선택
    const tableHeader = document.querySelector(".thst.grid2 th:last-child");
 
    if (sliderButton.style.left === "0px" || sliderButton.style.left === "") { 
        // 오른쪽으로 이동 (온실가스 배출량)
        sliderButton.style.left = "182px"; // 슬라이드 버튼 이동
        sliderTextLeft.style.color = "#286E71"; // 왼쪽 텍스트 검정색
        sliderTextRight.style.color = "#fff"; // 오른쪽 텍스트 흰색
        // 버튼 텍스트 변경 (온실가스 관련)
        button1.textContent = "전기(tCO₂)";
        button2.textContent = "가스(tCO₂)";
        
        // 현재 활성화된 버튼에 따라 테이블 헤더 업데이트
        if (button1.classList.contains("active")) {
            tableHeader.innerHTML = "전기 온실가스 배출량<br>(tCO₂)";
        } else {
            tableHeader.innerHTML = "가스 온실가스 배출량<br>(tCO₂)";
        }
    } else { 
        // 왼쪽으로 이동 (에너지 사용량)
        sliderButton.style.left = "0px"; // 슬라이드 버튼 원위치
        sliderTextLeft.style.color = "#fff"; // 왼쪽 텍스트 흰색
        sliderTextRight.style.color = "#286E71"; // 오른쪽 텍스트 검정색
        // 버튼 텍스트 변경 (에너지 관련)
        button1.textContent = "전기(MWh)";
        button2.textContent = "가스(천m³)";
        
        // 현재 활성화된 버튼에 따라 테이블 헤더 업데이트
        if (button1.classList.contains("active")) {
            tableHeader.innerHTML = "전기 에너지 사용량<br>(MWh)";
        } else {
            tableHeader.innerHTML = "가스 에너지 사용량<br>(천m³)";
        }
    } 
}
