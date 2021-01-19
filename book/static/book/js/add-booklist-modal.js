/**
 * Created by szhkai@qq.com on 17-6-8.
 */

var addBooklistModal = $("#addBooklistModal");

function triggerAddBooklist() {
    addBooklistModal.modal("show");
}

function actionAddBooklist() {
    var title = $("#addBooklistModalTitleInput").val().trim();
    var summary = $("#addBooklistModalSummaryTextarea").val().trim();
    var curActionUrl = "/booklist/add/";

    var postData = {
        name: title,
        summary: summary
    };

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