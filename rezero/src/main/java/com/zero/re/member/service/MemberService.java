package com.zero.re.member.service;

import com.zero.re.member.vo.MemberChartVO;
import com.zero.re.member.vo.MemberVO;

public interface MemberService {
	
	public MemberVO memLogin(MemberVO vo); 
	
	public MemberVO memRegist(MemberVO vo);
	
	public int idCheck(String id);
	
	public void memUpdate(MemberVO vo);
	
	public void memExit(String id);
	
	public MemberChartVO memberChart(String address);
}
