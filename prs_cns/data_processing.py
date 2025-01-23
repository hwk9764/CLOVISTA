import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(
        host="10.28.224.177",
        port="30634",
        database="postgres",
        user="postgres",
        password="0104",
        cursor_factory=RealDictCursor
    )

def get_performance_metrics(channel_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT AVG(v."videoViewCount"::float) as avg_views
        FROM "Channel" c
        JOIN "Video" v ON c.id = v.channel_id
        WHERE c.id = %s;
    """, (channel_id,))

    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_relation_metrics(channel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(CASE WHEN v."liveBroadcastContent" = 'true' THEN 1 END) as live_count
        FROM "Channel" c
        JOIN "Video" v ON c.id = v.channel_id
        WHERE c.id = %s;
    """, (channel_id,))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_revenue_metrics(channel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT COUNT(CASE WHEN v."hasPaidProductPlacement" = true THEN 1 END) as sponsored_count
        FROM "Channel" c
        JOIN "Video" v ON c.id = v.channel_id
        WHERE c.id = %s;
    """, (channel_id,))
    
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def import_from_db(channel_id, prompt_version):
    metrics_functions = {
        1: get_performance_metrics,
        2: get_relation_metrics,
        3: get_revenue_metrics
    }

    metrics = metrics_functions[prompt_version](channel_id)

    return metrics if metrics else {}
