package com.zero.re.member.dao;

import org.apache.ibatis.annotations.Mapper;

import com.zero.re.member.vo.MemberChartVO;
import com.zero.re.member.vo.MemberVO;

@Mapper
public interface IMemberDAO {
	public MemberVO memLogin(MemberVO vo);
	
	public void memRegist(MemberVO vo);
	
	public int idCheck(String id);
	
	public void memUpdate(MemberVO vo);
	
	public void memExit(String id);
	
	public MemberChartVO memberChart(String address);
}