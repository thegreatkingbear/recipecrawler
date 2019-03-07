# -*- coding: utf-8 -*-
import scrapy
from RecipeCrawler.items import RecipeItem, StepItem

class RecipeSpider(scrapy.Spider):
    name = 'recipe.py'

    # hand out every pages to "parse recipe list" method
    def start_requests(self):
        for i in range(1, 10): # 6304 is the last page
            url = 'http://www.10000recipe.com/recipe/list.html?order=accuracy&page={}'.format(i)
            request = scrapy.Request(url=url, callback=self.parseRecipeList)
            yield request

    # parse lists in the page into seperate recipes
    def parseRecipeList(self, response):
        #links = LinkExtractor(restrict_xpaths='//div[@class="recipe_list"]') # not sure how to use
        for link in response.xpath('//a[@class="thumbnail"]/@href').extract():
            url = 'http://www.10000recipe.com' + link
            request = scrapy.Request(url=url, callback=self.parseRecipe)
            yield request

    # hand over recipe link from previous method then parse it into items
    def parseRecipe(self, response):
        # prepare variables
        recipe = RecipeItem()
        main_ingredients = []
        sub_ingredients = []

        # dish image (original size)
        recipe['image_urls'] = [ response.xpath('//img[@id="main_thumbs"]').attrib['src'] ] # image pipeline only accepts list format

        # summary
        summary = response.xpath('//div[@class="view2_summary"]')
        recipe['title'] = summary.xpath('./h3/text()').extract_first()
        recipe['info_size'] = summary.xpath('.//span[@class="view2_summary_info1"]/text()').extract_first()
        recipe['info_time'] = summary.xpath('.//span[@class="view2_summary_info2"]/text()').extract_first()
        recipe['info_difficulty'] = summary.xpath('.//span[@class="view2_summary_info3"]/text()').extract_first()
        recipe['summary'] = summary.xpath('.//div[@class="view2_summary_in"]/descendant::text()[not(self::span)]').extract()

        # main ingredient (ready_ingre3)
        main_ingredient = response.xpath('//div[@class="ready_ingre3"]/ul[1]')
        for item in main_ingredient.xpath('./li'):
            ingredient = item.xpath('./text()').extract_first()
            material = item.xpath('./span/text()').extract_first()
            ingredient = ingredient.rstrip()
            if material is not None:
                ingredient = ingredient + '(' + material + ')'
            main_ingredients.append(ingredient)
        recipe['ingredients_main'] = main_ingredients

        # sub ingredient
        sub_ingredient = response.xpath('//div[@class="ready_ingre3"]/ul[2]')
        for item in sub_ingredient.xpath('./li'):
            ingredient = item.xpath('./text()').extract_first()
            material = item.xpath('./span/text()').extract_first()
            ingredient = ingredient.rstrip()
            if material is not None:
                ingredient = ingredient + '(' + material + ')'
            sub_ingredients.append(ingredient)
        recipe['ingredients_sub'] = sub_ingredients
        
        # main ingredient (cont_ingre)
        main_ingredient = response.xpath('//div[@class="cont_ingre"]/dl/dd/text()').extract_first()
        if main_ingredient is not None:
            main_ingredients = [x.strip() for x in main_ingredient.split(',')] # needs to be converted to list from string
            recipe['ingredients_main'] = main_ingredients

        # video (if exists)
        video_path = response.xpath('//*[@id="ifrmRecipeVideo"]')
        if video_path.get() is not None:
            video_src = video_path.attrib['org_src']
            if video_src is not None:
                recipe['video_url'] = video_src

        # steps 
        step_items = []
        for step in response.xpath('//div[starts-with(@id, "stepDiv")]'):
            stepItem = StepItem()
            stepItem['url'] = response.url # unique key for nested item
            text_step = step.xpath('.//text()').extract() # to get all texts in children
            text_step = ' '.join(text_step)
            stepItem['content'] = text_step
            image_step_path = step.xpath('./div[2]/img')
            if image_step_path.get() is not None:
                image_step = image_step_path.attrib['src']
                stepItem['image_urls'] = [ image_step ] # image pipeline only accepts list format
            step_items.append(stepItem)
            yield stepItem
        recipe['steps'] = step_items
        recipe['url'] = response.url # unique key for nested item

        # tags (if exists)
        tags = []
        tag_path = response.xpath('//div[@class="view_tag"]')
        if tag_path.get() is not None:
            tag_texts = tag_path.xpath('./a/text()').extract()
            for tag in tag_texts:
                tags.append(tag)
            recipe['tags'] = tags

        # tips (if exists)
        tips = []
        tips_texts = response.xpath('//dl[@class="view_step_tip"]/dd/text()').extract()
        print(tips_texts)
        for tip in tips_texts:
            tips.append(tip)
        recipe['tip'] = tips
        
        yield recipe

