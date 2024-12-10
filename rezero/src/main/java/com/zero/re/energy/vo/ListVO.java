package com.zero.re.energy.vo;

import java.util.List;

import lombok.Data;

@Data
public class ListVO {
	private List<EnergyVO> energyList;
    private List<EnergyVO> daejeonList;
    private List<EnergyVO> guList;
	private List<EnergyVO> energyGu;
	private List<EnergyVO> energyDong;
    
    public ListVO(List<EnergyVO> energyList, List<EnergyVO> daejeonList, 
    			  List<EnergyVO> guList, List<EnergyVO> energyGu,
    			  List<EnergyVO> energyDong) {
        this.energyList = energyList;
        this.daejeonList = daejeonList;
        this.guList = guList;
        this.energyGu = energyGu;
        this.energyDong = energyDong;
    }
}
