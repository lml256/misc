package com.news.entity;

import com.news.utils.MD5Util;

public class User {
	private int id;
	private String name;
	private String pass;
	private int admin;
	
	@Override
	public String toString() {
		return "User [id=" + id + ", name=" + name + ", pass=" + pass + ", admin=" + admin + "]";
	}
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getPass() {
		return MD5Util.MD5(pass);
	}
	public void setPass(String pass) {
		this.pass = pass;
	}
	public int getAdmin() {
		return admin;
	}
	public void setAdmin(int admin) {
		this.admin = admin;
	}
	
}
