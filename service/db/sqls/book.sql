# 删除图片 Path 的 /media 前缀
SELECT * FROM book_book WHERE id=3;

# UPDATE book_book
# SET pic = SUBSTR(pic, 7)
# WHERE id > 2 and id<8;
#
# UPDATE book_book
# SET pic = CONCAT('/', pic)
# WHERE id=8;
#
# UPDATE book_book
# SET pic = SUBSTR(pic, 2)
# WHERE id=1;



# UPDATE book_book
# SET pic = CONCAT('http://climg.szhkai.top', pic);