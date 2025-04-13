<script>
    let { children } = $props();
    import "$lib/style.css";
    // 可在此添加响应式状态管理（如需侧边栏折叠功能）
</script>

<div class="h-screen grid grid-rows-[auto_1fr] bg-gray-50">
    <!-- 顶部标题栏 -->
    <header class="sticky top-0">
        <!-- 导航栏组件 -->

        <div class="navbar bg-base-100 shadow-sm">
            <div class="flex-1">
                <a href="/" class="btn btn-ghost text-xl"
                    >大学生毕业论文（设计）管理系统</a
                >
            </div>
            <a class="mr-8" href="/system/system_front">前端服务检测</a>
            <a class="mr-8" href="/system/system_end">后端服务监测</a>
            <a class="mr-8" href="http://chat.deepseek.com">帮助</a>
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
                            <a class="justify-between">Profile</a>
                        </li>
                        <li><a>Settings</a></li>
                        <li><a>Logout</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </header>

    <!-- 主体区域 -->
    <div class="grid grid-cols-[auto_1fr] h-full">
        <!-- 侧边导航栏 -->
        <aside
            class="w-64 bg-white shadow-md sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto z-10 border-1"
        >
            <!-- 侧边栏组件 -->
            <div>
                <ul class="menu bg-white-200 rounded-box w-56 m-4">
                    <li class="text-center text-2xl m-0.5">管理员</li>
                    <li>
                        <details open>
                            <summary>系统管理</summary>
                            <ul>
                                <li><a href="/admin/time">时间管理</a></li>
                                <li><a href="/admin/user">用户管理</a></li>
                                <li><a href="/admin/selection">选题管理</a></li>
                                <li>
                                    <details close>
                                        <summary>保留样式</summary>
                                        <ul>
                                            <li><a>保留样式/a></li>
                                            <li><a>保留样式</a></li>
                                        </ul>
                                    </details>
                                </li>
                            </ul>
                        </details>
                    </li>
                    <li><a>保留样式</a></li>
                </ul>
            </div>
        </aside>

        <!-- 主内容区域 -->
        <main class="overflow-auto p-6">
            {@render children()}
        </main>
    </div>
</div>
