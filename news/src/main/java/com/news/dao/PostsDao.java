package com.news.dao;

import java.util.List;

import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import org.springframework.stereotype.Repository;

import com.news.entity.Posts;
import com.news.utils.SearchInfo;

@Repository
public interface PostsDao {

	@Select("select posts.*, user.name as username, target.name as targetname from posts, user, target where posts.userid =user.id and posts.target =target.id ${where} ${sort} ${limit}")
	public List<Posts> select(SearchInfo info);
	
	@Select("select * from posts where id=#{id}")
	public Posts getPosts(int id);
	
	@Insert("insert into posts(title, body, target, userid) values(#{title}, #{body}, #{target}, #{userid})")
	public void insert(Posts p);
	
	@Delete("delete from posts where id=#{id}")
	public void delete(int id);
	
	@Insert("update posts set title=#{title},body=#{body},target=#{target} where id=#{id}")
	public void update(Posts p);
}
