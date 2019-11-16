package com.news.dao;

import java.util.List;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import com.news.entity.User;

@Repository
public interface UserDao {
	@Select("select * from user")
	public List<User> select();
	
	@Select("select * from user where id=#{id}")
	public User getById(int id);
	
	@Select("select * from user where name=${name}")
	public User getUser(User u);
	
	@Select("select count(*) from user where name=#{name} and pass=#{pass}")
	public int login(User u);
	
	@Select("insert into user(name, pass) values(#{name},#{pass})")
	public void insert(User u);
	
	@Delete("delete from user where id=#{id}")
	public void delete(int id);
	
	@Insert("update user set pass=#{pass} where id=#{id}")
	public void update(User u);
}
