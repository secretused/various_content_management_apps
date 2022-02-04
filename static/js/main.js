// ページが読み込まれた後に実行
window.onload = () => {
    // toggleボタンをセレクト
    let sidebarToggler = document.getElementById('sidebarToggler')
    // let sidebarTogglerFa = document.getElementById('sidebarTogglerFa')
    let toggle_menu = document.getElementById('toggle_menu')

    toggle_menu.style.cssText = "left: 20px;"

    // 全ページを囲む親要素をセレクト
    let page = document.getElementsByTagName('main')[0];
    // page.style.cssText = 'margin-left: -200px'
    // 表示状態用の変数
    let showSidebar = false;

    let navbar = document.getElementById('navbar')
    let mainwrapper = document.getElementById('mainwrapper')

    // mainwrapper.style.cssText
    test = "height: " + (page.clientHeight - navbar.clientHeight) + "px";
    mainwrapper.style.cssText = test

    // イベント追加
    sidebarToggler.addEventListener('click', () => {

        // 表示状態判別
        if(showSidebar){

            // 閉じる
            toggle_menu.style.cssText = "left: 20px; transition: 0.3s all ease;"
            page.style.cssText = 'margin-left: 0px'
            // cardContent.style = "fas fa-times fa-lg";
            showSidebar = false;
            
            
        }else{

            // sidebarTogglerを✖︎に
            // sidebarTogglerFa.className = "fas fa-times fa-lg";
            // 削除
            // sidebarToggler.classList.remove( "fa-bars" ) ;
            // 開く
            toggle_menu.style.cssText = "left: 220px; transition: 0.3s all ease;"
            page.style.cssText = 'margin-left: 200px'
            showSidebar = true;

        }
    })
}