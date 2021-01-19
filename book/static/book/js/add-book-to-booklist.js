/**
 * Created by bovenson on 17-6-7.
 */

var addBookToOtherBooklistModal = $("#addBookToOtherBooklistModal");
var addBookToOtherBooklistModalBookId = $("#addBookToOtherBooklistModalBookId");
var addBookToOtherBooklistModalBookRemark = $("#addBookToOtherBooklistModalBookRemark");

var addBookToOtherBooklistModalBooklists = document.getElementById("addBookToOtherBooklistModalBooklists");

/* 点击书籍右侧的添加到书单 */
function addBookToOtherBooklist(bookId) {
    addBookToOtherBooklistModalBookId.val(bookId);
    // 获取书单列表
    var curActionUrl = "/user/booklist/get/";

    actionFunction();


    function actionFunction() {
        var ajaxOptions = {
            url: curActionUrl,
            type: "post",
            dataType: "json",
            dta: {},
            success: function (data) {
                if (data["res"] === "error") {
                    if (data["msg"] === "未登录") {
                        actionLogin();
                    } else {
                        alert(data["msg"]);
                    }
                } else if (data["res"] === "success") {
                    // 返回书单列表
                    var res_data = data["data"];
                    // console.log(res_data);
                    if (res_data.length > 0) {
                        addBookToOtherBooklistModalBooklists.innerHTML = "";
                        $("#addBookToOtherBooklistModalRemarkDiv").css("display", "block");
                        for (var i=0; i < res_data.length; ++i) {
                            addBookToOtherBooklistModalBooklists.innerHTML += createBooklistItemCheckbox(res_data[i].pk, res_data[i].fields.name);
                        }
                    }
                    // 显示模态框
                    addBookToOtherBooklistModal.modal("show");
                } else {
                    alert("服务器返回数据格式不正确")
                }
            },
            error: function (data) {
                alert("请求失败")
            }
        };
        // 发送请求
        $.ajax(ajaxOptions);
    }

    function createBooklistItemCheckbox(id, name) {
        var itemHtml = '<label class="CheckItem">' +
            '<input type="checkbox" class="CheckItem-input" name="selected-booklist" value="{id}">' +
            '<div class="CheckItem-box"><span class="Favlists-itemNameText">{name}</span></div></label>';
        // console.log(formatString(itemHtml, {id: id, name: name}));
        return formatString(itemHtml, {id: id, name: name})
    }

    String.prototype.format = function(replacements) {
        replacements = (typeof replacements === 'object') ? replacements : Array.prototype.slice.call(arguments, 0);
        return formatString(this, replacements);
    };

    var formatString = function (str, replacements) {
    replacements = (typeof replacements === 'object') ? replacements : Array.prototype.slice.call(arguments, 1);
    return str.replace(/\{\{|\}\}|\{(\w+)\}/g, function(m, n) {
        if (m === '{{') { return '{'; }
        if (m === '}}') { return '}'; }
        return replacements[n];
    });
};
}


/* 确认添加的书单 */
function confirmAddBookToOtherBooklist() {
    var curActionUrl = "/book/add-to-booklists/";
    var selectedItems = $("input[name=selected-booklist]");
    var postData = {
        book: addBookToOtherBooklistModalBookId.val(),
        booklists: [],
        remark: addBookToOtherBooklistModalBookRemark.val().trim()
    };
    for (var i=0; i < selectedItems.length; i++) {
        if (selectedItems.get(i).checked) {
            postData.booklists.push(selectedItems.get(i).value);
        }
    }

    var ajaxOptions = {
        url: curActionUrl,
        type: "post",
        dataType: "json",
        data: postData,
        success: function (data) {
            if (data["res"] === "error") {
                alert(data["msg"]);
            } else if (data["res"] === "success") {
                alert("添加成功");
            } else {
                alert("服务器返回数据格式不正确")
            }
        },
        error: function (data) {
            alert("请求失败")
        }
    };
    // 发送请求
    $.ajax(ajaxOptions);
}