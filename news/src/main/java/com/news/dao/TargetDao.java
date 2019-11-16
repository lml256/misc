package com.news.dao;

import java.util.List;

import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import com.news.entity.Target;

@Repository
public interface TargetDao {

	@Select("select * from target")
	public List<Target> select();
}
