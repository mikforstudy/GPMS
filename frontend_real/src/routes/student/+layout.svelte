<script>
  import { onMount } from 'svelte';
  let { children } = $props();
  import '$lib/style.css';

  let username = $state('');

  onMount(() => {
    if (typeof window !== 'undefined') {
      username = localStorage.getItem('username') || '用户';
    //   console.log(username);
      
    }
  });
</script>

<div class="h-screen grid grid-rows-[auto_1fr] bg-gray-50">
  <!-- 顶部标题栏 -->
<<<<<<< HEAD
  <header class="sticky top-0 z-50">
=======
  <header class="sticky top-0 ">
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645
            <!-- 导航栏组件 -->

        <div class="navbar bg-base-100 shadow-sm">
            <div class="flex-1">
                <a href="/student" class="btn btn-ghost text-xl"
                    >大学生毕业论文（设计）管理系统</a
                >
            </div>
            <a class="mr-8" href="/">欢迎回来, {username}!</a>
            <a class="mr-8" href="/">帮助</a>
            <div class="flex gap-4">
                <div class="dropdown dropdown-end">
                    <div
                        tabindex="0"
                        role="button"
                        class="btn btn-ghost btn-circle avatar"
                    >
                        <div class="w-10 rounded-full">
                            <img
                                alt="Tailwind CSS Navbar component"
                                src="https://img.tuxiangyan.com/uploads/allimg/2022053117/q335b2mpzhw.jpg"
                            />
                        </div>
                    </div>
                    <ul
                        tabindex="0"
                        class="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow"
                    >
                        <li>
                            <a href="/">Profile</a>
                        </li>
                        <li><a href="/student/change_password">修改密码</a></li>
                        <!-- 这是因为在点击“登出”链接时，SvelteKit 可能会使用客户端导航，
                         而不是完全重新加载页面。这意味着某些资源（如图片）可能不会立即重新加载。
                         要解决这个问题，可以在点击“登出”链接时强制浏览器进行完整的页面刷新。
<<<<<<< HEAD
                         可以通过在 <a> 标签上添加 rel="external" 属性来实现这一点。 -->
=======
                         你可以通过在 <a> 标签上添加 rel="external" 属性来实现这一点。 -->
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645
                        <li><a href="/login" rel="external">登出</a></li>
                    </ul>
                </div>
            </div>
        </div>
  </header>

  <!-- 主体区域 -->
  <div class="grid grid-cols-[auto_1fr] h-full">
    <!-- 侧边导航栏 -->
    <aside class="w-64 bg-white shadow-md sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto z-10 border-1">
        <!-- 侧边栏组件 -->
        <div>
            <ul class="menu bg-white-200 rounded-box w-56 m-4">
                <li class="text-center text-2xl m-0.5">学生</li>
                <li>
                    <details close>
                        <summary>首页管理</summary>
                        <ul>
                            <li><a href="/student">学生首页</a></li>
                            <li><a href="/student/notify">通知公告</a></li>
                            
                            <!-- <li><a href="/">保留样式</a></li> -->
                        </ul>
                    </details>
                </li>
                <li>
                    <details open>
                        <summary>选题分析</summary>
                        <ul>
<<<<<<< HEAD
                            <li><a href="http://47.94.225.78:8080/">选题分析</a></li>
=======
                            <li><a href="https://chat.deepseek.com/">选题分析</a></li>
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645
                        </ul>
                    </details>
                </li>
                <li>
                    <details open>
                        <summary>师生双选管理</summary>
                        <ul>
                            <li><a href="/student/declare">申报题目</a></li>
                            <li><a href="/student/my_title">我的题目</a></li>
                        </ul>
                    </details>
                </li>
                <li>
                    <details open>
                        <summary>过程文档管理</summary>
                        <ul>
                            <li><a href="/student/start">提交开题报告</a></li>
                            <li><a href="/student/middle">提交中期检查</a></li>
                            <li><a href="/student/process">提交过程稿</a></li>
                            <li><a href="/student/end">提交毕业论文（设计）最终版</a></li>
                        </ul>
                    </details>
                </li>
                <li>
                    <details open>
                        <summary>评审答辩和成绩管理</summary>
                        <ul>
                            <li><a href="/student/defense">查看我参加的答辩</a></li>
                            <li><a href="/student/defense_record">答辩记录</a></li>
                            <li><a href="/student/score">查看成绩</a></li>
                        </ul>
                    </details>
                </li>
<<<<<<< HEAD
                <li><a href="/student/export">导出所有文件</a></li>
=======
                <li><a href="/">待定</a></li>
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645
            </ul>
        </div>
    </aside>

    <!-- 主内容区域 -->
<<<<<<< HEAD
    <main class="overflow-auto p-4 z-0">
=======
    <main class="overflow-auto p-4">
>>>>>>> 47363d5289e4ea5cbd9a708e0f5c34c133007645
    {@render children()}
    </main>
  </div>
</div>