<script>
  import { onMount } from 'svelte';
  let { children } = $props();
  import '$lib/style.css';

  let username = $state('');

  onMount(() => {
    if (typeof window !== 'undefined') {
      username = localStorage.getItem('username') || '用户';
      console.log(username);
      
    }
  });
</script>

<div class="h-screen grid grid-rows-[auto_1fr] bg-gray-50">
  <!-- 顶部标题栏 -->
  <header class="sticky z-50 ">
            <!-- 导航栏组件 -->

        <div class="navbar bg-base-100 shadow-sm">
            <div class="flex-1">
                <a href="/teacher" class="btn btn-ghost text-xl"
                    >大学生毕业论文（设计）管理系统</a
                >
            </div>
            <a class="mr-8" href="#">欢迎回来, {username}!</a>
            <a class="mr-8" href="#">帮助</a>
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
                        <li><a href="/teacher/change_password">修改密码</a></li>
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
                <li class="text-center text-2xl m-0.5">教师</li>
                <li>
                    <details close>
                        <summary>首页管理</summary>
                        <ul>
                            <li><a href="/teacher/notify">通知公告</a></li>
                            <!-- <li><a href="/">保留样式</a></li> -->
                        </ul>
                    </details>
                </li>
                <li>
                    <details open>
                        <summary>选题分析</summary>
                        <ul>
                            <li><a href="http://47.94.225.78:8080/" target="_blank">选题分析</a></li>
                        </ul>
                    </details>
                </li>
                <li>
                    <details open>
                        <summary>师生双选管理</summary>
                        <ul>
                            <li><a href="/teacher/review_selection">审核学生申报题目</a></li>
                            <li><a href="/teacher/check_projects">查看学生项目</a></li>
                        </ul>
                    </details>
                </li>
                <li>
                    <details open>
                        <summary>过程文档管理</summary>
                        <ul>
                            <li><a href="/teacher/review_start">审核开题报告</a></li>
                            <li><a href="/teacher/review_middle">审核中期报告</a></li>
                            <li><a href="/teacher/process">查看学生过程稿</a></li>
                            <li><a href="/teacher/review_end">审核毕业论文（设计最终版）</a></li>
                        </ul>
                    </details>
                </li>
                <li>
                    <details open>
                        <summary>评审答辩和成绩管理</summary>
                        <ul>
                            <li><a href="/teacher/defense">查看我参加的答辩</a></li>
                            <!-- <li><a href="/">答辩记录</a></li>
                              -->
                            <li><a href="/teacher/score">成绩</a></li>
                            <li><a href="/teacher/score_docx">受邀评阅</a></li>
                        </ul>
                    </details>
                </li>
                <li><a href="/teacher/export">导出学生文件</a></li>
            </ul>
        </div>
    </aside>

    <!-- 主内容区域 -->
    <main class="overflow-auto p-6">
    {@render children()}
    </main>
  </div>
</div>