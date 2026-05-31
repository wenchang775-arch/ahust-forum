<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h4>关于我们</h4>
        <p>安徽理工大学校园贴吧，为师生提供便捷的交流平台</p>
      </div>
      <div class="footer-section">
        <h4>联系方式</h4>
        <p>地址：安徽省淮南市泰丰大街168号</p>
        <p>邮编：232001</p>
      </div>
      <div class="footer-section">
        <h4>友情链接</h4>
        <a href="https://www.ahust.edu.cn" target="_blank">安徽理工大学官网</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2024 安徽理工大学贴吧 - 校园交流社区</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  background: #2c3e50;
  color: white;
  padding: 40px 20px 20px;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.footer-section h4 {
  font-size: 16px;
  margin-bottom: 15px;
  color: #667eea;
}

.footer-section p {
  font-size: 14px;
  line-height: 1.8;
  color: #bdc3c7;
}

.footer-section a {
  color: #667eea;
  text-decoration: none;
  font-size: 14px;
}

.footer-section a:hover {
  text-decoration: underline;
}

.footer-bottom {
  max-width: 1200px;
  margin: 30px auto 0;
  padding-top: 20px;
  border-top: 1px solid #34495e;
  text-align: center;
}

.footer-bottom p {
  font-size: 14px;
  color: #95a5a6;
}
</style>