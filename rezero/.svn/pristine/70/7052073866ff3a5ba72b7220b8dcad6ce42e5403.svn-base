
<%
	/* ================================================================= 
	 * 작성일     : 2024. 11. 21. 
	 * 작성자     : 팽수
	 * 상세설명  : 
	 * 화면ID  :
	 * ================================================================= 
	 * 수정일         작성자             내용      
	 * ----------------------------------------------------------------------- 
	 * ================================================================= 
	 */
%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>

<!-- jQuery -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

<!-- Css -->
<link rel="stylesheet" href="resources/css/mystyles.css">

<!-- Bootstrap -->
<script
	src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<link
	href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
	rel="stylesheet" />
	
<!-- 주소 -->
<script src="//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</head>
<body>
	<!-- Top -->
    <nav class="navbar navbar-expand-lg bg-white">
        <div class="container-fluid">
			<!-- Logo -->
            <a class="navbar-brand" href="#!">
                <img src="resources/icon/logo.png" class="logo" alt="Logo">
            </a>
			<!-- Icons -->
			<div class="menu me-3">
				<c:if test="${sessionScope.login == null}">
					<a><img src="resources/icon/user-alt-fill@3x.png" id='nonLogin'class="icon"
						alt="mem Icon"></a>
				</c:if>
				<c:if test="${sessionScope.login != null}">
					<a><img src="resources/icon/menu@3x.png" id="myPage" class="icon" data-bs-toggle="offcanvas"
					data-bs-target="#offcanvasMyPage" aria-controls="offcanvasMyPage" alt="Menu Icon"></a>
				</c:if>
			</div>
		</div>
	</nav>

	<div class="modal fade" id="loginModal" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
		<div class="modal-dialog modal-dialog-centered">
			<div class="modal-content">
				<!-- LOGO -->
				<div class="logo pt-3" style="text-align: center;">
					<img src="resources/icon/logo.png" style="width: 160px;" alt="">
				</div>
	
				<!-- TOGGLE -->
				<div id="toggle-wrap">
					<div id="toggle-terms">
						<div id="cross">
							<span></span><span></span>
						</div>
					</div>
				</div>
	
				<!-- FORM -->
				<div class="form-wrap">
					<!-- TABS -->
					<div class="tabs">
						<h3 class="login-tab">
							<a class="log-in active" href="#login-tab-content">로그인</a>
						</h3>
						<h3 class="signup-tab">
							<a class="sign-up" href="#signup-tab-content">회원가입</a>
						</h3>
					</div>
	
					<!-- TABS CONTENT -->
					<div class="tabs-content">
						<!-- TABS CONTENT LOGIN -->
						<div id="login-tab-content" class="active">
							<form class="login-form" action="" method="post">
								<input type="text" class="input" id="id" autocomplete="off" name="id" placeholder="아이디">
								<input type="password" class="input" id="pw" autocomplete="off" name="pw" placeholder="비밀번호">
								<input type="checkbox" class="checkbox" checked id="remember_me">
								<label for="remember_me">자동로그인</label>
								<input type="button" class="button mt-5 mb-4 w-75" value="로그인" id="login">
							</form>
						</div>
	
						<!-- TABS CONTENT SIGNUP -->
						<div id="signup-tab-content">
							<form class="signup-form" action="" method="post">
								<input type="text" class="input" id="newId" autocomplete="off" placeholder="아이디" oninput="idCheck()">
								<span id="good" style="display: none; color: #6cae62;">사용 가능한 아이디 입니다.</span>
								<span id="bad" style="display: none; color: #dc3545;">이미 사용중인 아이디 입니다.</span>
								<input type="password" class="input" id="newPw" autocomplete="off" placeholder="비밀번호">
								<input type="text" class="input" id="newPlace" autocomplete="off" placeholder="주소">
								<input id="signUp" type="button" class="button my-4 w-75" value="회원가입">
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

</body>
<script type="text/javascript">
$(document).ready(function() {
	let isLoggedIn = false;  // 로그인 여부를 추적하는 변수
	
	$('#newPlace').click(execDaumPostcode);
	
	$(function(){
        $('#login').on("click",function (e) {
            e.preventDefault();
        	let id = $('#id').val();
            let pw = $('#pw').val();
            
            data={
            	'id': id,
            	'pw': pw
            }

            $.ajax({
                type: "post",
                url: "/login",
                data: JSON.stringify(data),
                contentType: 'application/json;',
                success: function (data) {
                	if(data == ''){
                		alert("올바르지 않은 계정 정보입니다");
                		$('.login-form')[0].reset();
                	}
                	else{
                		$('#loginModal').modal('hide');
                		$('.modal-backdrop').remove();  // 모달 뒤 배경 제거
                    	$('#nonLogin').attr('src',"resources/icon/menu@3x.png")
                    	isLoggedIn = true;  // 로그인 상태로 변경
                	}
                },
                error: function (request, status, error) {
                    console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                }
            });
        });
    });
	
	$(function(){
        $('#signUp').on("click",function () {
            
        	
        	let id = $('#newId').val();
            let pw = $('#newPw').val();
            let place = $('#newPlace').val();
            
            if(!id){
            	alert("아이디를 입력해주세요.");
		        return;
            }
            
            if(!pw){
            	alert("비밀번호를 입력해주세요.");
		        return;
            }
            
            if(!place){
            	alert("주소를 입력해주세요");
		        return;
            }
            
            if ($('#bad').css("display") === "block") {
            	alert("이미 사용중인 아이디 입니다.");
		        return;
            } 
            
            data={
            	'id': id,
            	'pw': pw,
            	'address': place
            }

            $.ajax({
                type: "post",
                url: "/regist",
                data: JSON.stringify(data),
                contentType: 'application/json;',
                success: function (data) {
                	$('#loginModal').modal('hide');
                	$('.modal-backdrop').remove();  // 모달 뒤 배경 제거
                	$('#nonLogin').attr('src',"resources/icon/menu@3x.png")
                	isLoggedIn = true;  // 로그인 상태로 변경
                },
                error: function (request, status, error) {
                    console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                }
            });
        });
        
     	// 이미지 클릭 시 이벤트
        $('#nonLogin').on("click", function () {
            if (isLoggedIn) {
                // 로그인된 상태에서 이미지 클릭 시 다른 이벤트 적용
                alert("로그인된 상태에서 이미지 클릭!");
                // 여기에 로그인된 후 실행할 다른 동작을 추가할 수 있습니다.
                // 예를 들어, 페이지 이동:
                // window.location.href = "/profile";
            } else {
                // 로그인되지 않은 상태에서 이미지 클릭 시 모달 표시
                $('#loginModal').modal('show');
            }
        });
     	
     	$('#myPage').on("click", function() {
     		alert("로그인된 상태에서 이미지 클릭!");
     	});
    });
});

function execDaumPostcode() {
	 new daum.Postcode({
		oncomplete: function(data) {
	            let addr = data.address;
	            $('#newPlace').val(addr);
		}
	}).open();
}

function idCheck() {
	let id = $('#newId').val();

	// 입력란의 값이 없으면 모든 span 태그 숨김
	if (id == "") {
		$('#good').css("display", "none");
		$('#bad').css("display", "none");
		return;
	}
	
	$.ajax({
		type : 'post',
		url : '/idCheck',
		data : {
			id : id
		},
		success : function(cnt) { 
			if (cnt == 0) { // cnt가 0일 경우 -> 사용 가능한 아이디 
				$('#good').css("display", "block")
				$('#bad').css("display", "none")
			} else { // cnt가 1일 경우 -> 이미 존재하는 아이디
				$('#bad').css("display", "block")
				$('#good').css("display", "none")
			}
		},
		error : function() {
			alert("아이디 확인 중 오류가 발생했습니다.");
		}
	});
}
</script>
</html>