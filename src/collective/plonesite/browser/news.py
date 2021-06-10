# -*- coding: utf-8 -*-
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class NewsListingView(BrowserView):

    template = ViewPageTemplateFile('templates/news_listing.pt')

    def __call__(self):
        return self.template()

    def get_image_url(self, context, request, width=1200, height=800, direction='down', fallback=False):  # noqa: 501
        """Return Image URL of Image in Context or given object"""
        try:
            image = context.image
        except AttributeError:
            image = None

        image_url = None
        if image:
            if image.contentType in ['image/svg+xml', 'image/webp']:
                image_url = context.absolute_url() + '/@@images/image'
            else:
                view = api.content.get_view('images', context, request)
                image = view.scale('image', width=width, height=height, direction=direction)  # noqa: 501
                image_url = image.absolute_url()
        else:
            if fallback:
                portal = api.portal.get().absolute_url()
                image_url = portal + '/++plone++collective.plonesite/plone-news-logo.png'  # noqa: 501

        return image_url

    def crop(self, text, count):
        """Crop given text to given count"""
        cropped_text = ' '.join((text[0:count].strip()).split(' ')[:-1])
        strips = ['.', ',', ':', ';']
        for s in strips:
            cropped_text = cropped_text.strip(s)
        if len(text) > count:
            return cropped_text + u'...'
        return text

    def get_items(self):
        results = []
        items = api.content.find(
            portal_type='News Item',
            review_state='published',
            sort_on='Date',
            sort_order='descending',
            context=api.portal.get(),
        )[:25]
        for item in items:
            item = item.getObject()
            image = self.get_image_url(item, self.request, width=600, height=400, fallback=True)
            data = {
                'title': self.crop(item.title, 100),
                'description': self.crop(item.description, 200),
                'date': api.portal.get_localized_time(datetime=item.Date()),
                'image': image,
                'url': item.absolute_url(),
            }
            results.append(data)
        return results
