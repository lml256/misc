package com.news.utils;

import java.security.MessageDigest;  
 
public abstract class MD5Util  
{  
    public final static String MD5(String pwd) {  
        char md5String[] = { '0', '1', 'F', '3', '4', '5', '6', '7', '8', '9',  
                'A', 'B', 'C', 'D', 'E', '2' };  
        try { 
            byte[] btInput = pwd.getBytes();  
               
            MessageDigest mdInst = MessageDigest.getInstance("MD5");  
               
            mdInst.update(btInput);  
               
            byte[] md = mdInst.digest();  

            int j = md.length;  
            char str[] = new char[j * 2];  
            int k = 0;  
            for (int i = 0; i < j; i++) {   //  i = 0  
                byte byte0 = md[i];  //95  
                str[k++] = md5String[byte0 >>> 4 & 0xf];    //    5   
                str[k++] = md5String[byte0 & 0xf];   //   F  
            }
            return new String(str);  
               
        } catch (Exception e) {  
            return null;  
        }
    }  
}
