/*
 * 公用js
 * File: common.js
 * Author: szhkai@qq.com
 * */


/* _navigation.html */
$(document).ready(function () {

    // 跨域请求保护
    var csrftoken = $.cookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // 登录注册
    var loginBtnElement = $("#btn-login");
    var registerBtnElement = $("#btn-register");
    var registerOrLoginTipElement = $("#registerOrLoginTipElement");
    var registerOrLoginBtnElement = $("#registerOrLoginBtnElement");
    var inputEmailElement = $("#inputEmail");
    var inputPasswordElement = $("#inputPassword");
    var lrModalErrorTipElement = $("#lrModalErrorTipElement");

    var registerStrTip = "还没有账号? 点击注册";
    var loginStrTip = "已有账号? 点击登录";
    var registerStr = "注册";
    var loginStr = "登录";

    loginBtnElement.click(loginBtnClick);
    registerBtnElement.click(registerBtnClick);
    registerOrLoginTipElement.click(actionTipClick);
    registerOrLoginBtnElement.click(actionLoginOrRegister);

    function loginBtnClick() {
        changeTextToLogin();
        $("#loginRegisterModelBox").modal("show");
    }

    function registerBtnClick() {
        changeTextToRegister();
        $("#loginRegisterModelBox").modal("show");
    }

    // 登录操作
    function actionLoginOrRegister() {
        var tStr = registerOrLoginBtnElement.text();
        var loginUrl = "/user/login/";
        var registerUrl = "/user/register/";
        var curActionUrl = "";

        // 置空错误提示
        lrModalErrorTipElement.text("");

        // 获取输入
        var email = inputEmailElement.val();
        var password = inputPasswordElement.val();
        if (tStr === loginStr) {
            curActionUrl = loginUrl;
        } else if (tStr === registerStr) {
            curActionUrl = registerUrl;
        }

        var postData = {
            email: email,
            username: email,
            nickname: email,
            password: password
        };

        var ajaxOptions = {
            url: curActionUrl,
            type: "post",
            dataType: "json",
            data: postData,
            success: function(data) {
                if (data["res"] === "error") {
                    setErrorTip(data["msg"]);
                } else if (data["res"] === "success") {
                    // 登录/注册 成功, 刷新页面
                    location.reload();
                } else {
                    setErrorTip("服务器返回数据格式不正确")
                }
            },
            error: function() {
                setErrorTip("请求失败")
            }
        };

        // 发送请求
        $.ajax(ajaxOptions);
    }

    function setErrorTip(msg) {
        lrModalErrorTipElement.text(msg);
    }

    function actionTipClick() {
        var tStr = registerOrLoginBtnElement.text();
        if (tStr === loginStr) {
            changeTextToRegister();
        } else if (tStr === registerStr) {
            changeTextToLogin();
        }
    }

    function changeTextToLogin() {
        lrModalErrorTipElement.text("");
        registerOrLoginBtnElement.text(loginStr);
        registerOrLoginTipElement.text(registerStrTip);
    }

    function changeTextToRegister() {
        lrModalErrorTipElement.text("");
        registerOrLoginBtnElement.text(registerStr);
        registerOrLoginTipElement.text(loginStrTip);
    }


    /** 点击用户名显示popover窗体 **/
    var usernameElement = $("#usernameElement");
    var userPopoverModal = $("#userPopoverModal");
    var userPopoverModalNode = document.getElementById("userPopoverModal");
    // 绑定事件
    usernameElement.click(showUserPopover);
    // 显示弹出层
    function showUserPopover(event) {
        console.log(event);
        var clientX = event.target.offsetWidth / 2 - userPopoverModalNode.offsetWidth / 2 + event.target.offsetLeft;
        var clientY = event.target.offsetTop + event.target.clientHeight + 18;
        console.log(clientY);
        userPopoverModal.css('visibility', 'visible');
        userPopoverModal.css('top', clientY + "px"); // 63px
        userPopoverModal.css('left', clientX + "px");
    }


    // 监听页面时间
    document.onmousedown = function (event) {
        // console.log(userPopoverModalNode);
        // console.log(event.srcElement);
        // 如果点击位置在弹出框内
        if (isParent(userPopoverModalNode, event.srcElement)) {
        } else { // 否则
            userPopoverModal.css('visibility', 'hidden');
        }
    };

    // 页面大小改变时
    window.onresize = function(){
        // 隐藏popover窗体
        userPopoverModal.css('visibility', 'hidden');
    };

    // 判断ea是不是eb的父节点
    function isParent(ea, eb) {
        while (eb.parentNode) {
            eb = eb.parentNode;
            if (ea === eb) {
                return true;
            }
        }
        return false;
    }
});

/* 确定/取消模态框 */
function showConfirmOrCancelModal(title, msg, confirm, cancel) {
    var confirmCancelModal = $("#confirmCancelModal");
    var confirmCancelModalTitle = $("#confirmCancelModalTitle");
    var confirmCancelModalText = $("#confirmCancelModalText");
    var confirmCancelModalConfirm = $("#confirmCancelModalConfirm");

    confirmCancelModalTitle.text(title);
    confirmCancelModalText.text(msg);
    confirmCancelModalConfirm.unbind('click');
    // 点击确定, 回调函数
    confirmCancelModalConfirm.click(confirm);
    confirmCancelModal.modal("show");
}

function actionLogin() {
    $("#btn-login").click();
}