# Several errors on PostgreSQL build with Valgrind

- URL: https://github.com/documentdb/documentdb/issues/369
- Repo: documentdb/documentdb (language: C)
- State: open; created 2025-11-05T09:02:13Z; status ok; passes offcwe

## Issue body

reporter (NONE) · yehoto · 2025-11-05T09:02:13Z · https://github.com/documentdb/documentdb/issues/369

**Describe the bug**
Conditional jump or move depends on uninitialised value(s), Invalid read of size 16

**Environment**
- Operating system and version: Ubuntu 24.04 LTS
- PostgreSQL version: 17
- Architecture: x86_64 (64-bit)

**Reproduction Steps**

(Run [build_documentdb_with_valgrind.sh] to build with Valgrind) 
1. Create ~/run.sh: 
```
PG_VERSION_USED=17 $HOME/documentdb/scripts/start_oss_server.sh -d /tmp/pgsql/data -c
psql -h 127.0.0.1 -d postgres -p 9712 -f ~/test.sql
$HOME/pgsql17/bin/pg_ctl -D /tmp/pgsql/data -m immediate stop
grep -A 40 "VALGRINDERROR-BEGIN" /tmp/pgsql/data/pglog.log
```
2. Run ~/run.sh with Valgrind:
```
valgrind --quiet --exit-on-first-error=yes --error-markers=VALGRINDERROR-BEGIN,VALGRINDERROR-END --error-exitcode=1 --leak-check=no --time-stamp=yes --track-origins=yes --gen-suppressions=all --trace-children=yes --suppressions=$HOME/documentdb-deps/postgres-repo/17/src/tools/valgrind.supp  ~/run.sh
```

Content of test.sql:

Case1:
```
set documentdb.defaultUseCompositeOpClass to on;

SELECT documentdb_api.insert_one('comp_db', 'comp_collection', FORMAT('{ "_id": 8, "a": { "key": "%s" }, "b": "%s" }', repeat('a', 10000), repeat('a', 10000))::bson);
SELECT documentdb_api_internal.create_indexes_non_concurrently(
    'comp_db', '{ "createIndexes": "comp_collection", "indexes": [ { "name": "a_1_b_1_c_1_comp", "key": { "a": 1, "b": 1, "c": 1} } ] }', TRUE);
```
Case2:
```
select documentdb_api.shard_collection('db', 'removeme', '{"a":"hashed"}', false);
select count(*) from documentdb_api.collection('db', 'removeme');
```
Case3:
```
CREATE SCHEMA and3;
SET search_path TO documentdb_core,documentdb_api,documentdb_api_catalog,documentdb_api_internal,public,and3;
SELECT 1 FROM insert_one('db','and3', '{"a":"foo"}');
CREATE OR REPLACE FUNCTION and3.checkScanMatch(query bson, examined_row_count int, expected_row_count int)
 RETURNS void
 LANGUAGE plpgsql
AS $$
DECLARE
        returned_row_count int;
BEGIN
        SELECT count(*) INTO returned_row_count
        FROM collection('db','and3') WHERE document @@ query;
END;
$$;
SELECT checkScanMatch('{"a": {"$regularExpression":{"pattern":"a","options":""}}}', 0, 0);
```

Case4:
```
select bson_dollar_project('{"_id":"1","a":"APPLE", "b":"app", "c" : "i"}', '{"result" : { "$regexFindAll" : {"input":"$a", "regex" : "$b", "options" :"$c" }} }');
```

Case5:
```
SELECT documentdb_api.insert_one('db', 'index_truncation_tests', '{"_id": 26, "ikey" : [ "String before", 1234, 1234, "This is a string after the numbers" ]}');

SELECT document FROM documentdb_api.collection('db', 'index_truncation_tests') WHERE document @@ '{ "ikey": { "$elemMatch": { "$all": [ { "$regex": "limit$", "$options": "" } ] }}}';
```

Case6:
```
SET search_path TO documentdb_core,documentdb_api,documentdb_api_catalog,documentdb_api_internal;
SELECT insert_one('db','regex', '{"_id" : 105, "b" : "xyz800", "description" : "this is Multiple\n in\bcline \bdescription" }');
SELECT document from collection('db', 'regex') where document @@ '{"description": {"$regex": " line ","$options": "i"}}';

```

**Expected behavior**

No Valgrind errors in any of the cases (i.e., grep returns no output)

**Actual behavior**
Case1:
```
==00:00:01:14.863 74566== VALGRINDERROR-BEGIN
==00:00:01:14.863 74566== Conditional jump or move depends on uninitialised value(s)
==00:00:01:14.863 74566==    at 0x85C7262: GetIndexTermMetadata (bson_gin_entrypoint.c:1185)
==00:00:01:14.863 74566==    by 0x85BD15A: BuildSinglePathTermsForCompositeTerms (bson_gin_composite_entrypoint.c:1924)
==00:00:01:14.863 74566==    by 0x85BD2F1: GenerateCompositeTermsCore (bson_gin_composite_entrypoint.c:1958)
==00:00:01:14.863 74566==    by 0x85BE51D: gin_bson_composite_path_extract_value (bson_gin_composite_entrypoint.c:141)
==00:00:01:14.864 74566==    by 0x6AC42B: FunctionCall5Coll (fmgr.c:1242)
==00:00:01:14.864 74566==    by 0x8733BE6: rumExtractEntries (rumutil.c:767)
==00:00:01:14.864 74566==    by 0x873084D: rumHeapTupleBulkInsert (ruminsert.c:508)
==00:00:01:14.864 74566==    by 0x8730C45: rumBuildCallback (ruminsert.c:580)
==00:00:01:14.864 74566==    by 0x22C278: heapam_index_build_range_scan (heapam_handler.c:1706)
==00:00:01:14.864 74566==    by 0x872FFE2: table_index_build_scan (tableam.h:1785)
==00:00:01:14.864 74566==    by 0x873109E: rumbuild (ruminsert.c:671)
==00:00:01:14.864 74566==    by 0x85A472F: extension_rumbuild_core (rum.c:1200)
==00:00:01:14.864 74566==  Uninitialised value was created by a heap allocation
==00:00:01:14.864 74566==    at 0x6D2426: palloc (mcxt.c:1340)
==00:00:01:14.864 74566==    by 0x85BD0AE: BuildSinglePathTermsForCompositeTerms (bson_gin_composite_entrypoint.c:1903)
==00:00:01:14.864 74566==    by 0x85BD2F1: GenerateCompositeTermsCore (bson_gin_composite_entrypoint.c:1958)
==00:00:01:14.864 74566==    by 0x85BE51D: gin_bson_composite_path_extract_value (bson_gin_composite_entrypoint.c:141)
==00:00:01:14.864 74566==    by 0x6AC42B: FunctionCall5Coll (fmgr.c:1242)
==00:00:01:14.864 74566==    by 0x8733BE6: rumExtractEntries (rumutil.c:767)
==00:00:01:14.864 74566==    by 0x873084D: rumHeapTupleBulkInsert (ruminsert.c:508)
==00:00:01:14.864 74566==    by 0x8730C45: rumBuildCallback (ruminsert.c:580)
==00:00:01:14.864 74566==    by 0x22C278: heapam_index_build_range_scan (heapam_handler.c:1706)
==00:00:01:14.864 74566==    by 0x872FFE2: table_index_build_scan (tableam.h:1785)
==00:00:01:14.864 74566==    by 0x873109E: rumbuild (ruminsert.c:671)
==00:00:01:14.864 74566==    by 0x85A472F: extension_rumbuild_core (rum.c:1200)
==00:00:01:14.864 74566== 
==00:00:01:14.864 74566== VALGRINDERROR-END


```
Case2:
```
==00:00:01:16.257 73707== VALGRINDERROR-BEGIN
==00:00:01:16.258 73707== Conditional jump or move depends on uninitialised value(s)
==00:00:01:16.258 73707==    at 0x4BD43B: compare_path_costs_fuzzily (pathnode.c:173)
==00:00:01:16.258 73707==    by 0x4BDAFE: add_path (pathnode.c:452)
==00:00:01:16.258 73707==    by 0x486FC8: get_index_paths (indxpath.c:745)
==00:00:01:16.258 73707==    by 0x487A23: create_index_paths (indxpath.c:279)
==00:00:01:16.258 73707==    by 0x478060: set_plain_rel_pathlist (allpaths.c:783)
==00:00:01:16.258 73707==    by 0x478147: set_rel_pathlist (allpaths.c:499)
==00:00:01:16.258 73707==    by 0x47822C: set_base_rel_pathlists (allpaths.c:351)
==00:00:01:16.258 73707==    by 0x4787E7: make_one_rel (allpaths.c:221)
==00:00:01:16.258 73707==    by 0x49C92E: query_planner (planmain.c:280)
==00:00:01:16.258 73707==    by 0x4A37E3: grouping_planner (planner.c:1553)
==00:00:01:16.258 73707==    by 0x4A4D53: subquery_planner (planner.c:1122)
==00:00:01:16.258 73707==    by 0x4A52BD: standard_planner (planner.c:416)
==00:00:01:16.258 73707==  Uninitialised value was created by a stack allocation
==00:00:01:16.258 73707==    at 0x47D42B: cost_index (costsize.c:551)
==00:00:01:16.258 73707== 
==00:00:01:16.258 73707== VALGRINDERROR-END


```

Case3:
```
==00:00:01:43.431 74378== VALGRINDERROR-BEGIN
==00:00:01:43.431 74378== Conditional jump or move depends on uninitialised value(s)
==00:00:01:43.431 74378==    at 0x123A9E04: ???
==00:00:01:43.431 74378==    by 0x1182C42F: ???
==00:00:01:43.431 74378==  Uninitialised value was created by a stack allocation
==00:00:01:43.431 74378==    at 0x860552D: bson_dollar_regex (bson_dollar_operators.c:980)
==00:00:01:43.431 74378== 
==00:00:01:43.431 74378== VALGRINDERROR-END

```

Case4:
```
==00:00:01:28.537 196007== VALGRINDERROR-BEGIN
==00:00:01:28.537 196007== Conditional jump or move depends on uninitialised value(s)
==00:00:01:28.537 196007==    at 0x11B7BC6E: ???
==00:00:01:28.537 196007==    by 0x7AA9B20: ???
==00:00:01:28.537 196007==    by 0x7AA9B20: ???
==00:00:01:28.537 196007==    by 0x7AA9B22: ???
==00:00:01:28.537 196007==    by 0x1179C177: ???
==00:00:01:28.537 196007==    by 0x7AA9B20: ???
==00:00:01:28.537 196007==  Uninitialised value was created by a stack allocation
==00:00:01:28.537 196007==    at 0x80A7AFA: PgbsonToSinglePgbsonElement (pgbsonelement.c:86)
==00:00:01:28.537 196007== 
==00:00:01:28.537 196007== VALGRINERROR-END

```

Case5:
```
==00:00:00:49.582 119919== VALGRINDERROR-BEGIN
==00:00:00:49.582 119919== Invalid read of size 16
==00:00:00:49.582 119919==    at 0x123A9C60: ???
==00:00:00:49.582 119919==    by 0x118743D4: ???
==00:00:00:49.582 119919==  Address 0x118743ef is 95 bytes inside a block of size 106 client-defined
==00:00:00:49.582 119919==    at 0x6D2426: palloc (mcxt.c:1340)
==00:00:00:49.582 119919==    by 0x1F05E1: detoast_attr (detoast.c:184)
==00:00:00:49.582 119919==    by 0x6AD3DB: pg_detoast_datum (fmgr.c:1835)
==00:00:00:49.582 119919==    by 0x86051E0: bson_dollar_elemmatch (bson_dollar_operators.c:800)
==00:00:00:49.582 119919==    by 0x3BC347: ExecInterpExpr (execExprInterp.c:764)
==00:00:00:49.582 119919==    by 0x3C9F4A: ExecEvalExprSwitchContext (executor.h:357)
==00:00:00:49.582 119919==    by 0x3C9F4A: ExecQual (executor.h:426)
==00:00:00:49.582 119919==    by 0x3CA1A1: ExecScan (execScan.c:225)
==00:00:00:49.582 119919==    by 0x3D71A3: ExecBitmapHeapScan (nodeBitmapHeapscan.c:585)
==00:00:00:49.582 119919==    by 0x3C70BA: ExecProcNodeFirst (execProcnode.c:464)
==00:00:00:49.582 119919==    by 0x3BFF81: ExecProcNode (executor.h:275)
==00:00:00:49.582 119919==    by 0x3C002E: ExecutePlan (execMain.c:1648)
==00:00:00:49.582 119919==    by 0x3C0B29: standard_ExecutorRun (execMain.c:360)
==00:00:00:49.582 119919== 
==00:00:00:49.582 119919== VALGRINERROR-END

```

Case6:
```
==00:00:01:00.196 247915== VALGRINDERROR-BEGIN
==00:00:01:00.196 247915== Invalid read of size 16
==00:00:01:00.196 247915==    at 0x123ADCA4: ???
==00:00:01:00.196 247915==    by 0x11A6227F: ???
==00:00:01:00.196 247915==  Address 0x11a6229f is 79 bytes inside a block of size 89 client-defined
==00:00:01:00.196 247915==    at 0x7542DE: palloc (mcxt.c:1340)
==00:00:01:00.196 247915==    by 0x1F2B77: detoast_attr (detoast.c:184)
==00:00:01:00.196 247915==    by 0x72A3B7: pg_detoast_datum (fmgr.c:1835)
==00:00:01:00.196 247915==    by 0x8609619: bson_dollar_regex (bson_dollar_operators.c:981)
==00:00:01:00.196 247915==    by 0x3F3DD9: ExecInterpExpr (execExprInterp.c:764)
==00:00:01:00.196 247915==    by 0x3EFD73: ExecInterpExprStillValid (execExprInterp.c:1927)
==00:00:01:00.196 247915==    by 0x403725: ExecEvalExprSwitchContext (executor.h:357)
==00:00:01:00.196 247915==    by 0x403725: ExecQual (executor.h:426)
==00:00:01:00.196 247915==    by 0x4039DE: ExecScan (execScan.c:225)
==00:00:01:00.196 247915==    by 0x412882: ExecBitmapHeapScan (nodeBitmapHeapscan.c:585)
==00:00:01:00.196 247915==    by 0x400471: ExecProcNodeFirst (execProcnode.c:464)
==00:00:01:00.196 247915==    by 0x3F83A5: ExecProcNode (executor.h:275)
==00:00:01:00.196 247915==    by 0x3F8452: ExecutePlan (execMain.c:1648)
==00:00:01:00.196 247915== 
==00:00:01:00.196 247915== VALGRINERROR-END

```
**Additional context**

Similarly, Case1's  error occurs with these queries:

```
SELECT documentdb_api_internal.create_indexes_non_concurrently('prep_unique_db', '{ "createIndexes": "collection", "indexes": [ { "name": "a_1", "key": { "a": 1 }, "storageEngine": { "enableOrderedIndex": true, "buildAsUnique": true } } ] }', TRUE);
select COUNT(documentdb_api.insert_one('prep_unique_db', 'collection', FORMAT('{ "a": %s, "b": %s }', i, 100-i)::bson)) FROM generate_series(1, 100) i;

```

```
SELECT COUNT(documentdb_api.insert_one('comp_db2', 'skip_entry_asc', FORMAT('{ "_id": %s, "a": %s, "b": %s, "c": %s }', ((i * 100) + (j * 10) + k), i, j, k)::bson)) FROM generate_series(1, 5) i, generate_series(1, 10) j, generate_series(1, 100) k;
SELECT documentdb_api_internal.create_indexes_non_concurrently('comp_db2', '{ "createIndexes": "skip_entry_asc", "indexes": [ { "key": { "a": 1, "b": 1, "c": 1 }, "name": "a_1", "enableOrderedIndex": true } ] }', TRUE);

```

```
SELECT documentdb_api.insert_one('hint_db', 'query_index_hints', '{ "_id": 1, "a": 1, "c": 1 }');
SELECT documentdb_api_internal.create_indexes_non_concurrently('hint_db', '{ "createIndexes": "query_index_hints", "indexes": [ { "key": { "a": 1 }, "enableCompositeTerm": true, "name": "a_3" }] }', true);
```

```
SELECT documentdb_api_internal.create_indexes_non_concurrently('comp_elmdb',
    '{ "createIndexes": "cmp_elemmatch_ops", "indexes": [ { "key": { "price": 1 }, "name": "price_1", "enableCompositeTerm": true }, { "key": { "brands": 1 }, "name": "brands_1", "enableCompositeTerm": true } ] }', TRUE);
SELECT documentdb_api.insert_one('comp_elmdb', 'cmp_elemmatch_ops', '{ "_id": 1, "price": [ 120, 150, 100 ] }');

```
```
SELECT COUNT(documentdb_api.insert_one('db', 'ttlCompositeOrderedScan', FORMAT('{ "_id": %s, "ttl": { "$date": { "$numberLong": "1657900030774" } } }', i, i)::documentdb_core.bson)) FROM generate_series(10, 10000) AS i;

SELECT documentdb_api_internal.create_indexes_non_concurrently('db', '{"createIndexes": "ttlCompositeOrderedScan", "indexes": [{"key": {"ttl": 1}, "enableCompositeTerm": true, "name": "ttl_index", "v" : 1, "expireAfterSeconds": 5, "sparse": true}]}', true);

```
Similarly, Case2's error occurs with these queries:

```
SELECT documentdb_api.shard_collection('db', 'agg_pipeline_samplerate', '{ "_id": "hashed" }', false);
SELECT document FROM bson_aggregation_pipeline('db', '{ "aggregate": "agg_pipeline_samplerate", "pipeline": [ { "$match": { "$sampleRate": 1 } }, {"$count": "count"} ], "cursor": {} }');
```
```
SELECT documentdb_api.shard_collection('db', 'agg_pipeline_movie_catalog', '{ "_id": "hashed" }', false);

SELECT document FROM bson_aggregation_pipeline('db',
    '{ "aggregate": "agg_pipeline_movie_screenings", "pipeline": [ { "$lookup": { "from": "agg_pipeline_movie_catalog", "as": "matched_docs", "pipeline": [ { "$count": "efe" } ] } } ], "cursor": {} }');

```

```
SELECT documentdb_api.shard_collection('db', 'testAggregatesWithIndex', '{ "_id": "hashed" }', false);

BEGIN;
set local enable_seqscan to off;
set local documentdb.forceUseIndexIfAvailable to on;
SELECT BSONSUM('{ "": 1 }') FROM documentdb_api.collection('db', 'testAggregatesWithIndex');
ROLLBACK;

```

```
SELECT documentdb_api_internal.create_indexes_non_concurrently('idx_only_scan_db', '{ "createIndexes": "idx_only_scan_coll", "indexes": [ { "key": { "country": 1, "provider": 1 }, "storageEngine": { "enableOrderedIndex": true }, "name": "country_provider_1" }] }', true);

EXPLAIN (ANALYZE ON, COSTS OFF, VERBOSE ON, TIMING OFF, SUMMARY OFF) SELECT document FROM bson_aggregation_pipeline('idx_only_scan_db', '{ "aggregate" : "idx_only_scan_coll", "pipeline" : [{ "$match" : {"provider": {"$eq": "AWS"}} }, { "$count": "count" }]}');

```

```
SELECT documentdb_api.shard_collection('db', 'coll_delete_sort', '{ "a": "hashed" }', false);

SELECT collection_id AS coll_delete_sort FROM documentdb_api_catalog.collections WHERE database_name = 'db' AND collection_name = 'coll_delete_sort' \gset
SELECT documentdb_api_internal.delete_worker(
    p_collection_id=>:coll_delete_sort,
    p_shard_key_value=>:coll_delete_sort,
    p_shard_oid => 0,
    p_update_internal_spec => '{ "deleteOne": { "query": { "_id": "dog" }, "collation": "en-u-ks-level3",  "sort": { "_id": 1 }, "returnDocument": 1, "returnFields": { "a": 0} } }'::bson,
    p_update_internal_docs=>null::bsonsequence,
    p_transaction_id=>null::text
) FROM documentdb_api.collection('db', 'coll_delete_sort');
```
```
SELECT documentdb_api_internal.create_indexes_non_concurrently(
  'mydb',
  '{
     "createIndexes": "collection_i",
     "indexes": [
       {
         "key": {"a.$**": 1}, "name": "my_idx_1",
         "partialFilterExpression":
         {
           "b": {"$gte": 10}
         }
       }
     ]
   }',
   true
);

SELECT documentdb_api_internal.create_indexes_non_concurrently(
   true
);

  EXPLAIN (COSTS OFF) SELECT COUNT(*)
  FROM documentdb_api.collection('mydb', 'collection_i')
  WHERE document @@ '
  {
    "$and": [
      { "b": {"$gte": 10} }
    ]
  }
  ';
```
```
select documentdb_api.shard_collection('db', 'into', '{"_id":"hashed"}', false);

select count(*) from documentdb_api.collection('db','into') where document @@ '{}';
```
Best regards,
Anna Likhtinfeld
Postgres Professional (http://postgrespro.com/)

<!-- Hidden links -->
[build_documentdb_with_valgrind.sh]: https://github.com/yehoto/build_DocumentDB/blob/main/build_documntdb_with_valgrind.sh
[start_oss_server.sh]: https://github.com/documentdb/documentdb/blob/main/scripts/start_oss_server.sh


## Comment 4185072749

other (CONTRIBUTOR) · xgerman · 2026-04-03T20:25:53Z · https://github.com/documentdb/documentdb/issues/369#issuecomment-4185072749

@visridha  wonder if this is addressed and we can close

## Comment 4340035973

other (NONE) · documentdb-triage-tool[bot] · 2026-04-29T00:24:38Z · https://github.com/documentdb/documentdb/issues/369#issuecomment-4340035973

<!-- bot:documentdb-triage-tool kind:auto-label v:1 -->
🤖 Auto-triaged by [documentdb-triage-tool](https://github.com/patty-chow/documentdb-maintainer-bot).

**Applied:** `engine`, `bug`
**Project fields suggested:** Component `core` · Priority `P1` · Effort `L` · Status `In Progress`
**Confidence:** 0.75 (llm)

<details><summary>Reasoning</summary>

LLM: Multiple Valgrind-detected memory errors (uninitialized reads, invalid reads) across several code paths including indexing, aggregation/regex, and collection operations — these are latent memory safety bugs affecting correctness and stability.

</details>

If a label is wrong, remove it manually and ping `@patty-chow` so the rules can be tuned. The bot will not re-label items that already have component labels.

## Comment 4583199579

other (NONE) · documentdb-triage-tool[bot] · 2026-05-30T15:06:51Z · https://github.com/documentdb/documentdb/issues/369#issuecomment-4583199579

👋 @visridha — this issue has been assigned for 29 days with no activity. Is it still in progress? If you've made progress, please leave a quick update. Otherwise it'll be flagged for re-assignment at the next triage meeting.

<!-- bot:stale-ping v:1 -->

## Comment 4698988524

other (NONE) · documentdb-triage-tool[bot] · 2026-06-13T15:42:56Z · https://github.com/documentdb/documentdb/issues/369#issuecomment-4698988524

👋 @visridha — this issue has been assigned for 14 days with no activity. Is it still in progress? If you've made progress, please leave a quick update. Otherwise it'll be flagged for re-assignment at the next triage meeting.

<!-- bot:stale-ping v:1 -->

## Comment 4826525183

other (NONE) · documentdb-triage-tool[bot] · 2026-06-28T15:17:27Z · https://github.com/documentdb/documentdb/issues/369#issuecomment-4826525183

👋 @visridha — this issue has been assigned for 14 days with no activity. Is it still in progress? If you've made progress, please leave a quick update. Otherwise it'll be flagged for re-assignment at the next triage meeting.

<!-- bot:stale-ping v:1 -->

## Comment 4960250103

other (NONE) · documentdb-triage-tool[bot] · 2026-07-13T16:32:44Z · https://github.com/documentdb/documentdb/issues/369#issuecomment-4960250103

👋 @visridha — this issue has been assigned for 15 days with no activity. Is it still in progress? If you've made progress, please leave a quick update. Otherwise it'll be flagged for re-assignment at the next triage meeting.

<!-- bot:stale-ping v:1 -->

## Comment 5302641757

other (NONE) · documentdb-triage-tool[bot] · 2026-08-15T14:20:41Z · https://github.com/documentdb/documentdb/issues/369#issuecomment-5302641757

👋 @visridha — this issue has been assigned for 14 days with no activity. Is it still in progress? If you've made progress, please leave a quick update. Otherwise it'll be flagged for re-assignment at the next triage meeting.

<!-- bot:stale-ping v:1 -->

## Comment 5463844568

other (NONE) · documentdb-triage-tool[bot] · 2026-08-29T17:30:43Z · https://github.com/documentdb/documentdb/issues/369#issuecomment-5463844568

👋 @visridha — this issue has been assigned for 14 days with no activity. Is it still in progress? If you've made progress, please leave a quick update. Otherwise it'll be flagged for re-assignment at the next triage meeting.

<!-- bot:stale-ping v:1 -->

## Comment 5654808118

other (NONE) · documentdb-triage-tool[bot] · 2026-09-13T17:17:08Z · https://github.com/documentdb/documentdb/issues/369#issuecomment-5654808118

👋 @visridha — this issue has been assigned for 14 days with no activity. Is it still in progress? If you've made progress, please leave a quick update. Otherwise it'll be flagged for re-assignment at the next triage meeting.

<!-- bot:stale-ping v:1 -->

## Comment 5858376583

other (NONE) · documentdb-triage-tool[bot] · 2026-09-27T18:03:14Z · https://github.com/documentdb/documentdb/issues/369#issuecomment-5858376583

👋 @visridha — this issue has been assigned for 14 days with no activity. Is it still in progress? If you've made progress, please leave a quick update. Otherwise it'll be flagged for re-assignment at the next triage meeting.

<!-- bot:stale-ping v:1 -->
