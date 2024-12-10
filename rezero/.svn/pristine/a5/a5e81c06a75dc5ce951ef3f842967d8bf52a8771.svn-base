package com.zero.re.member.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.zero.re.member.dao.IMemberDAO;
import com.zero.re.member.vo.MemberChartVO;
import com.zero.re.member.vo.MemberVO;

@Service("memberService")
public class MemberServiceImpl implements MemberService{
	
	@Autowired
	IMemberDAO dao;
	
	@Override
	public MemberVO memLogin(MemberVO vo) {
		MemberVO login = dao.memLogin(vo);
		
		return login;
	}
	
	@Override
	public MemberVO memRegist(MemberVO vo) {
		dao.memRegist(vo);
		MemberVO login = dao.memLogin(vo);
		return login;
	}
	
	@Override
	public int idCheck(String id) {
		int cnt = dao.idCheck(id);
		return cnt;
	}
	
	@Override
	public void memUpdate(MemberVO vo) {
		dao.memUpdate(vo);
	};
	
	@Override
	public void memExit(String id){
		dao.memExit(id);
	};
	
	
	@Override
	public MemberChartVO memberChart(String address) {
		// "대전" 제거 로직
	    if (address == null || address.trim().isEmpty()) {
	        throw new IllegalArgumentException("Adress cannot be null or empty");
	    }
	    
	    if (address.startsWith("대전")) {
	    	address = address.substring(2).trim(); // "대전" 제거
	    }

	    // DAO 호출
	    MemberChartVO chart = dao.memberChart(address);

	    return chart;
	}
	
}