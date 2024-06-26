from django.shortcuts import render, redirect
from posts.models import Post, Like, Comment
from profiles.models import Profile
from posts.forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import json


# Create your views here.
@login_required
def post_comment_create_and_list_view(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    # Post form, comment form
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False
    error = False

    if 'submit_p_form' in request.POST:
        print(request.POST.get('submit_p_form'))
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostModelForm()
            post_added = True
        else:
            error = p_form.errors

    # if 'submit_c_form' in request.POST:
    #     print(request.POST)
    #     c_form = CommentModelForm(request.POST)
    #     if c_form.is_valid():
    #         instance = c_form.save(commit=False)
    #         instance.user = profile
    #         instance.post = Post.objects.get(id=request.POST.get('post_id'))
    #         instance.save()
    #         c_form = CommentModelForm()
    #         return redirect(request.META.get('HTTP_REFERER'))

    if request.method == 'POST' and 'submit_p_form' not in request.POST:
        data = json.loads(request.body)
        if 'submit_c_form' in data:
            post_id = data['post_id']
            body = data['body']
            post = Post.objects.get(id=post_id)
            comment = Comment(user=profile, post=post, body=body)
            if body != "":
                comment.save()
            c_form = CommentModelForm()
            comments = Post.objects.get(id=post_id).num_comments()
            name = profile.user.username
            pic_url = profile.avatar.url
            cmnt_date = comment.created
            date = comment.created.strftime("%d-%b-%Y %I:%M %p")
            ctx = {
                'comments': comments, 
                'name': name, 
                'pic_url': json.dumps("http://127.0.0.1:8000/"+pic_url),
                'year': json.dumps(cmnt_date.year), 
                'month': json.dumps(cmnt_date.month), 
                'date': date 
            }
            print(date)
            return JsonResponse(ctx)
    ctx = {
        'posts': posts, 
        'profile': profile, 
        'p_form': p_form, 
        'c_form': c_form, 
        'post_added': post_added, 
        'error': error
    }
    return render(request, 'posts/main.html', ctx)

@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data['post_id']
        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post.liked.all():
            post.liked.remove(profile)
        else:
            post.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'
        post.save()
        like.save()
        likes = json.dumps(post.num_likes())
        return JsonResponse({'likes':likes})
    return redirect('posts:main-post-view')


class PostdeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('posts:main-post-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, "Opps! You are not the author of this post.")
            print(messages)
        return obj


class PostUpdateView(UpdateView, LoginRequiredMixin):
    form_class = PostModelForm
    # fields = ['content', 'image']
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "Opps! You are not the author of this post.")
            return super().form_invalid(form)
        
# login_required        
# def test_view(request):
#     data = json.loads(request.body)
#     post = Post.objects.get(id=data['post_id'])
#     print(post)
#     return JsonResponse(data, safe=False)



