/**
 * File: booklistdetail.js
 * Created by bovenson on 17-6-5.
 */

/* 书单 */
function editBookListTrigger() {
    var editBooklistBoxElement = $("#editBooklistBoxElement");
    var inputEditBookListTitleElement = $("#inputEditBookListTitleElement");
    var textareaBookList = $("#textareaBookList");
    var booklistNameElement = $("#booklistNameElement");
    var booklistSummaryElement = $("#booklistSummaryElement");

    if (editBooklistBoxElement.css("display") === "none") {
        // 显示修改框
        editBooklistBoxElement.css("display", "block");
        // 设置编辑区显示内容
        inputEditBookListTitleElement.val(booklistNameElement.text());
        textareaBookList.val(booklistSummaryElement.text());
    } else {
        editBooklistBoxElement.css("display", "none");
    }
}

function editBookList(booklistId) {
    var curActionUrl = "/booklist/update/";

    var booklistNameElement = $("#booklistNameElement");
    var booklistSummaryElement = $("#booklistSummaryElement");
    var editBooklistBoxElement = $("#editBooklistBoxElement");
    var inputEditBookListTitleElement = $("#inputEditBookListTitleElement");
    var textareaBookList = $("#textareaBookList");

    var postData = {
        booklist: booklistId,
        name: inputEditBookListTitleElement.val().trim(),
        summary: textareaBookList.val().trim()
    };

    var ajaxOptions = {
        url: curActionUrl,
        type: "post",
        dataType: "json",
        data: postData,
        success: function (data) {
            if (data["res"] === "error") {
                setErrorTipBookList(data["msg"]);
            } else if (data["res"] === "success") {
                // 修改/添加评语成功
                // 更新
                booklistNameElement.text(inputEditBookListTitleElement.val());
                booklistSummaryElement.text(textareaBookList.val());
                // 隐藏编辑框
                editBookListTrigger();
            } else {
                setErrorTipBookList("服务器返回数据格式不正确")
            }
        },
        error: function (data) {
            setErrorTipBookList("请求失败")
        }
    };

    // 发送请求
    $.ajax(ajaxOptions);

    function setErrorTipBookList(msg) {
        var errorTipEditBookListElement = $("#errorTipEditBookListElement");
        errorTipEditBookListElement.text(msg);
    }
}

/* 删除书单 */
function deleteBookList(booklistId) {
    var curActionUrl = "/booklist/delete/";
    var postData = {
        booklist: booklistId
    };

    showConfirmOrCancelModal("删除书单", "确定要删除该书单吗?", actionDeleteBookList);

    function actionDeleteBookList() {
        var ajaxOptions = {
            url: curActionUrl,
            type: "post",
            dataType: "json",
            data: postData,
            success: function (data) {
                if (data["res"] === "error") {
                    alert(data["msg"]);
                } else if (data["res"] === "success") {
                    window.location.href = '/';
                } else {
                }
            },
            error: function () {
                    alert("请求失败");
            }
        };
        // 发送请求
        $.ajax(ajaxOptions);
    }
}

/* 向书单中添加书籍 */
function addBookToBooklist() {
    var addBookModal = $("#addBookModal");
    addBookModal.modal("show");

    var addBookModalSearchBody = $("#addBookModalSearchBody");
    var addBookModalInfoBody = $("#addBookModalInfoBody");
    addBookModalSearchBody.css("display", "block");
    addBookModalInfoBody.css("display", "none");
}

function deleteBookFromBooklist(bookId, booklistId) {
    var curActionUrl = "/booklist/book/delete/";
    showConfirmOrCancelModal("删除书籍", "确定要从书单中删除该书籍吗?", actionDeleteBookFromBookList);

    var postData = {
        booklist: booklistId,
        book: bookId
    };
    function actionDeleteBookFromBookList() {
            var ajaxOptions = {
                url: curActionUrl,
                type: "post",
                dataType: "json",
                data: postData,
                success: function (data) {
                    if (data["res"] === "error") {
                        alert(data["msg"]);
                    } else if (data["res"] === "success") {
                        $("#booklistItemContainer" + bookId).css("display", "none");
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
}

function confirmAddBookToBooklist() {
    var bookId = $("#addBookModalBookId").val();
    var booklistId = $("#booklistIdHiddenInput").val();
    var addBookModalBookRemarkTextArea = $("#addBookModalBookRemarkTextArea");

    // 向书单添加书籍
    // console.log(bookId);
    // console.log(booklistId);

        // 从服务器获取书籍数据
    var postData = {
        book: bookId,
        booklist: booklistId,
        remark: addBookModalBookRemarkTextArea.val().trim()
    };

    var ajaxOptions = {
        url: "/booklist/book/add/",
        type: "post",
        dataType: "json",
        data: postData,
        success: function (data) {
            if (data["res"] === "error") {
                alert(data["msg"]);
            } else if (data["res"] === "success") {
                // 修改/添加评语成功
                // setErrorTip("成功");
                $("#addBookModal").modal("hide");
                location.reload();
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

/* 获取书籍信息 */
function getBookInfo() {
    var addBookModalBookNameInput = $("#addBookModalBookNameInput");
    var addBookModalSearchBody = $("#addBookModalSearchBody");
    var addBookModalInfoBody = $("#addBookModalInfoBody");
    var inputText = addBookModalBookNameInput.val();

    setErrorTip("");

    function setModalBookInfo(book) {
        var addBookModalInfoBodyImg = $("#addBookModalInfoBodyImg");
        var addBookModalInfoBodySummary = $("#addBookModalInfoBodySummary");
        var addBookModalInfoBodyTitle = $("#addBookModalInfoBodyTitle");
        var addBookModalInfoBodyAuthor = $("#addBookModalInfoBodyAuthor");
        var addBookModalInfoBodyTag = $("#addBookModalInfoBodyTag");
        var addBookModalInfoBodyScore = $("#addBookModalInfoBodyScore");
        var addBookModalBookId = $("#addBookModalBookId");

        addBookModalInfoBodyTitle.text(book["name"]);
        addBookModalInfoBodyImg.attr("src", book["pic"]);
        addBookModalInfoBodySummary.text(book["summary"].substring(0, 100));
        addBookModalInfoBodyScore.text(book["score"]);
        addBookModalBookId.val(book["id"]);

        // 作者
        document.getElementById('addBookModalInfoBodyAuthor').innerHTML = "";
        for (var i=0; i < book["author"].length; ++i) {
            var newA = document.createElement("a");
            // console.log(newA);
            // console.log(book["author"][i]);
            newA.className = "link-a";
            newA.style.marginRight = "5px";

            newA.href = "javascript: void(0)";
            newA.text = book["author"][i].name;
            document.getElementById('addBookModalInfoBodyAuthor').appendChild(newA);
        }


        // 标签
        document.getElementById('addBookModalInfoBodyTag').innerHTML = "";
        for (var j=0; j < book["tag"].length && j < 5; ++j) {
            var newA = document.createElement("a");
            // console.log(newA);
            // console.log(book["tag"][j]);
            newA.className = "link-a";
            newA.style.marginRight = "5px";

            newA.href = "javascript: void(0)";
            newA.text = "#" + book["tag"][j].name;
            document.getElementById('addBookModalInfoBodyTag').appendChild(newA);
        }
    }

    function setErrorTip(msg) {
        var addBookModalErrorTip = $("#addBookModalErrorTip");
        addBookModalErrorTip.text(msg);
    }

    // 从服务器获取书籍数据
    var postData = {
        url: inputText
    };

    var ajaxOptions = {
        url: "/book/url/",
        type: "post",
        dataType: "json",
        data: postData,
        success: function (data) {
            if (data["res"] === "error") {
                setErrorTip(data["msg"]);
            } else if (data["res"] === "success") {
                // 修改/添加评语成功
                // setErrorTip("成功");
                // 设置信息
                setModalBookInfo(data["data"]);
                // 设置显示隐藏
                addBookModalSearchBody.css("display", "none");
                addBookModalInfoBody.css("display", "block");
            } else {
                setErrorTip("服务器返回数据格式不正确")
            }
        },
        error: function (data) {
            setErrorTipBookRemark("请求失败")
        }
    };

    // 发送请求
    $.ajax(ajaxOptions);
}

/* 评语 */
function editBookRemarkTrigger(bookId) {
    var bookRemarkBlock = $("#block-book-remark-" + bookId);
    // console.log(bookRemarkBlock.css("display"));
    if (bookRemarkBlock.css("display") === "none") {
        // 显示修改框
        bookRemarkBlock.css("display", "block");
        // 设置textarea内容
        $("#textarea-book-remark-" + bookId).val($("#bookRemarkAlready" + bookId).text());
    } else {
        bookRemarkBlock.css("display", "none");
    }
}

function editBookRemark(booklistId, bookId, remarkId) {
    var curActionUrl = "/book-remark";

    var textareaBookRemark = $("#textarea-book-remark-" + bookId);
    var spanBookRemarkAlready = $("#bookRemarkAlready" + bookId);
    var updateBookRemarkDiv = $("#updateBookRemarkDiv" + bookId);
    var addBookRemarkDiv = $("#addBookRemarkDiv" + bookId);
    // console.log(booklistId);
    // console.log(bookId);
    // console.log(remarkId);
    // console.log(textareaBookRemark.val());
    var postData = {
        booklist: booklistId,
        book: bookId,
        content: textareaBookRemark.val().trim()
    };

    var ajaxOptions = {
        url: curActionUrl,
        type: "post",
        dataType: "json",
        data: postData,
        success: function (data) {
            if (data["res"] === "error") {
                setErrorTipBookRemark(data["msg"]);
            } else if (data["res"] === "success") {
                // 修改/添加评语成功
                // setErrorTipBookRemark("成功");
                // 更新
                spanBookRemarkAlready.text(textareaBookRemark.val());
                // 隐藏编辑框
                editBookRemarkTrigger(bookId);

                // 设置 (修改, 删除), (添加评语, 删除) div
                // 如果评语为空
                if (postData.content.length === 0) {
                    updateBookRemarkDiv.css("display", "none");
                    addBookRemarkDiv.css("display", "block");
                } else {
                    updateBookRemarkDiv.css("display", "block");
                    addBookRemarkDiv.css("display", "none");
                }
            } else {
                setErrorTipBookRemark("服务器返回数据格式不正确")
            }
        },
        error: function (data) {
            setErrorTipBookRemark("请求失败")
        }
    };
    
    // 发送请求
    $.ajax(ajaxOptions);

    function setErrorTipBookRemark(msg) {
        var errorTipBookRemarkElement = $("#errorTipBookRemark" + bookId);
        errorTipBookRemarkElement.text(msg);
    }
}

