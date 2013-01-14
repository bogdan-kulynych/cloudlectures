{
    "type":"object",
    "$schema": "http://json-schema.org/draft-03/schema",
    "id": "#",
    "required":false,
    "properties":{
        "units": {
            "type":"array",
            "id": "units",
            "required":false,
            "items":
                {
                    "type":"object",
                    "id": "0",
                    "required":false,
                    "properties":{
                        "name": {
                            "type":"string",
                            "id": "name",
                            "required":true,
                            "title": "Unit name"
                        },
                        "lectures": {
                            "type":"array",
                            "id": "lectures",
                            "required":false,
                            "items":
                                {
                                    "type":"object",
                                    "id": "0",
                                    "required":false,
                                    "properties":{
                                        "title": {
                                            "type":"string",
                                            "id": "title",
                                            "required":true,
                                            "title": "Title"
                                        },
                                        "description": {
                                            "type":"string",
                                            "id": "description",
                                            "required":false,
                                            "title": "Description"
                                        },
                                        "video_url": {
                                            "type":"string",
                                            "id": "video_url",
                                            "required":true,
                                            "title": "Video URL"
                                        }
                                    }
                                }
                        }
                    }
                }
        }
    }
}