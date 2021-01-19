/**
 * Created by bovenson on 17-6-8.
 */

var nicknameInputElement = $("#nicknameInputElement");
var passwordInputElement = $("#passwordInputElement");
var newPasswordInputElement = $("#newPasswordInputElement");
var newPasswordRepeatInputElement = $("#newPasswordRepeatInputElement");

function actionUpdateProfile() {
    var curActionUrl = "/user/profile/update/";

    var nickname = nicknameInputElement.val();
    var password = passwordInputElement.val();
    var newPassword = newPasswordInputElement.val();
    var newPasswordRepeat = newPasswordRepeatInputElement.val();

    // 从服务器获取书籍数据
    var postData = {
        nickname: nickname,
        password: password,
        newPassword: newPassword,
        newPasswordRepeat: newPasswordRepeat
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
                // 修改/添加评语成功
                // setErrorTip("成功");
                alert("修改成功!");
                location.href = "/";
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