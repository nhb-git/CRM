from django.db import models


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    alias = models.CharField(verbose_name='url别名', max_length=32, unique=True)
    url = models.CharField(verbose_name='含正则的URL', max_length=128, null=True, blank=True)
    is_menu = models.BooleanField(verbose_name='是否可以做菜单', default=False)
    icon = models.CharField(verbose_name='图标', max_length=32, null=True, blank=True)
    parent_menu = models.ForeignKey(verbose_name='父菜单标志', to='self', null=True, on_delete=models.CASCADE, blank=True)
    # parent_menu = models.ManyToManyField(
    #     to='self',
    #     verbose_name='父导航标志',
    #     null=True,
    #     blank=True,
    # )

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role', blank=True)

    def __str__(self):
        return self.name
