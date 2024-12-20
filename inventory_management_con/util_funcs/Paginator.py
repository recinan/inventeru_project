from django.core.paginator import Paginator


class PaginatorClass:
    @staticmethod
    def paginator(request,list, paginator_count:int,page_name:str):
        p = Paginator(list,paginator_count)
        page = request.GET.get(page_name)
        out_list = p.get_page(page)
        return out_list